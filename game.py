import random as rand
SUITS = "♥♦♠♣"
VALUES = "123456789JQK"
PHASES = ["Bet Phase", "Burn and Swap Phase", "Show Phase"]
SPECIAL_INPUT=['p','P']

def index_to_card(index):
  suit = SUITS[round((index + 1) / 12) - 1]
  value = VALUES[((index + 1) % 4) - 1]
  return "[" + suit + value + "]"

def index_to_value(index):
  return ((index + 1) % 4) - 1

def index_to_suit(index):
  return round((index + 1) / 12) - 1

class deck:
  def __init__(self):
    self.drawn = [];
    self.decksize = 52;
    self.phase = PHASES[0]
    for x in range(0,52):
      self.drawn.append("Dealer")

  def draw_n_times(self, new_owner, times):
    for x in range(times):
      selection = rand.randint(0,51)
      while(self.drawn[selection] != "Dealer"):
        selection = rand.randint(0,51)
      self.drawn[selection] = new_owner
      self.decksize-=1

  def draw(self, new_owner):
    self.draw_n_times(new_owner, 1)
    
  def give(self, index, new_owner):
    print(self.drawn[index] + " to " + new_owner)
    self.drawn[index] = new_owner
    
  def shuffle(self, from_owner):
    for x in range(0,52):
      if(self.drawn[x] == from_owner or from_owner == "All" and self.drawn[x] != "Dealer"):
        self.drawn[x] = "Dealer"
        self.decksize+=1
        
  def find_num_owner(self, owner):
    stack_size = 0
    for x in range(0,52):
      if self.drawn[x] == owner:
        stack_size +=1
    return stack_size

  def show_owner(self, owner):
    for x in range(0,52):
      if self.drawn[x] == owner:
        print(index_to_card(x), end =" ")
    print("")
    
  def show_owner_hidden(self, owner):
    for x in range(0,52):
      if self.drawn[x] == owner:
        print("[//]", end =" ")
    print("")

  def show_stacks(self, owner):
    converted = owner
    if owner == "Dealer":
      converted = "Deck"
    if owner == "Pot":
      converted = "Bets"
    stack_size = self.find_num_owner(owner)
    ten_stacks = round(stack_size / 10)
    without_tens = ten_stacks % 10
    if stack_size < 10:
      without_tens = stack_size
    for w in range(1, without_tens):
      print("[", end='')
    if stack_size >= 1:
      print("[" +converted + ":" + str(stack_size) + "]", end='')
    print("")


  def show_score(self,player):
    score = "High Card"
    values = []
    royals = [0,0,0,0]
    suit_totals = [0,0,0,0]
    for v in range(0,12):
      values.append(0)
    for x in range(0,52):
      if self.drawn[x] == player:
        value = index_to_value(x)
        suit = index_to_suit(x)
        values[value] += 1
        suit_totals[suit] += 1
        if value >= 10:
          royals[12-value] += 1
    if 2 in values:
      score = "One Pair"
    if 3 in values:
      score = "Three of a kind"
    if values.count(2) == 2:
      score = "Two Pair"
    if values.count(2) == 3:
      score = "Three Pair"
    if 5 in suit_totals:
      score = "Flush"
    print(score, end ="       ")
    
        

  def show_table(self, player):
    burn_prompt = "Burn a card into hand"
    if self.phase == "Bet Phase":
      burn_prompt = "Bet a card from stack"
    if self.phase == "Show Phase":
      burn_prompt = "To Fold: "
    self.show_stacks("opponent\'s stack")
    self.show_owner_hidden("opponent")
    print("")
    print("")
    print("")
    print("\t\t\t\t Phase: " + self.phase + " [Enter P to pass]")
    self.show_stacks("Dealer")
    self.show_stacks("Pot")
    print("")
    print("")
    print("")
    print("")
    print("")
    self.show_owner(player)
    next_card = self.find_num_owner(player)
    if self.phase == "Show Phase":
      self.show_score(player)
    else:
      for x in range(1, next_card + 1):
        print(str(x) + "    ", end = "")
    if(self.find_num_owner(player + "\'s stack") >= 1):
      print(str(next_card + 1) + ": " + burn_prompt)
    self.show_stacks(player + "\'s stack")

  def find_next(self, owner):
    for x in range(0,52):
      if self.drawn[x] == owner:
        return x
    return -1
  
  def find_next_index(self, owner, index):
    current = 0
    for x in range(0,52):
      if self.drawn[x] == owner:
        if current + 1 == index:
          return x
        current+=1
    return -1

  def win(self, player):
    for x in range(0,52):
      if self.drawn[x] == "Pot":
        self.give(x, player + "\'s stack")
  
  def clear_screen(self):
    for x in range(60):
      print("")
  
  def next_phase(self):
    self.phase = PHASES[((PHASES.index(self.phase) + 1) % len(PHASES))]
    
  def menu(self, selection, player):
    self.clear_screen()
    self.show_table(player)
    prompt = "Enter a number to swap/select: "
    if self.phase == "Bet Phase":
      prompt = "Select a card to use as betting chip: "
    if selection == 0:
      select = input(prompt)
      if select in SPECIAL_INPUT:
        return self.menu(select, player)
      return self.menu(int(select), player)
    elif selection == self.find_num_owner(player) + 1:
      if self.phase == "Show Phase":
        self.shuffle(player)
        self.draw_n_times(player,5)
        self.next_phase()
        return self.menu(0, player)
      elif self.phase == "Bet Phase":
        self.give(self.find_next(player + "\'s stack"), "Pot")
        return self.menu(0,player)
      self.give(self.find_next(player + "\'s stack"), player)
      return self.menu(0, player)
    elif selection == 'P' or selection == 'p':
      self.next_phase()
      self.menu(0,player)
    else:
      if self.phase == "Show Phase":
        self.win(player)
        self.shuffle(player)
        self.draw_n_times(player,5)
        self.next_phase()
        return self.menu(0, player)
      elif self.phase == "Bet Phase":
        self.give(self.find_next_index(player, int(selection)),"Pot")
        return self.menu(0, player)
      self.give(self.find_next_index(player, int(selection)), "Discard")
      self.draw(player)
      return self.menu(0, player)
      
  def start_game(self, player, opponent):
    self.draw_n_times(player,5)
    self.draw_n_times(opponent,5)
    self.draw_n_times(player + "\'s stack", 3)
    self.draw_n_times(opponent + "\'s stack", 3)
    self.menu(0, player)


if __name__ == "__main__":
  test_deck = deck()
  test_deck.start_game("me","opponent")
  
