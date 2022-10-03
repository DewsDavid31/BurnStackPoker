import random as rand
SUITS = "♥♦♠♣"
VALUES = "A23456789TJQK"
PHASES = ["Bet Phase", "Burn and Swap Phase", "Show Phase","Draw Phase"]
SPECIAL_INPUT=['p','P', 'f', 'F']

def index_to_card(index):
  suit = SUITS[round((index + 1) / 13) - 1]
  value = VALUES[((index + 1) % 13) - 1]
  return "[" + suit + value + "]"

def index_to_value(index):
  return ((index + 1) % 13)

def index_to_suit(index):
  return round((index + 1) / 13)

class deck:
  def __init__(self):
    self.swaps = 0
    self.drawn = [];
    self.decksize = 52;
    self.phase = PHASES[0]
    self.winner = "None"
    for x in range(0,52):
      self.drawn.append("Dealer")

  def draw_n_times(self, new_owner, times):
    if self.decksize <= times:
      self.shuffle("Discard")
    for x in range(times):
      selection = rand.randint(0,51)
      while(self.drawn[selection] != "Dealer"):
        selection = rand.randint(0,51)
      self.drawn[selection] = new_owner
      self.decksize-=1

  def draw(self, new_owner):
    self.draw_n_times(new_owner, 1)
    
  def give(self, index, new_owner):
    self.drawn[index] = new_owner
    
  def shuffle(self, from_owner):
    for x in range(1,52):
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
    for x in range(1,52):
      if self.drawn[x] == owner:
        print(index_to_card(x), end =" ")
    print("")
    
  def show_owner_hidden(self, owner):
    for x in range(1,52):
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
    score = "Nothing"
    values = []
    royals = [0,0,0,0]
    suit_totals = [0,0,0,0]
    streak = 0
    straight = 0
    for v in range(0,12):
      values.append(0)
    for x in range(0,52):
      if self.drawn[x] == player:
        value = index_to_value(x)
        suit = index_to_suit(x)
        values[value - 1] += 1
        suit_totals[suit - 1] += 1
        if value == 11:
          royals[1] += 1
        if value == 12:
          royals[2] += 1
        if value == 0:
          royals[3] +=1
        if value == 1:
          royals[0] += 1
    for s in range(0,12):
      if values[s] > 0:
        streak += 1
      if values[s] <= 0:
        streak = 0
      if streak >= 5:
        straight = 1
    if sum(values[10:]) > 0:
      score = "High Card"
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
    if straight >= 1:
      score = "Straight"
    if 5 in suit_totals and straight >=1:
      score = "Straight Flush"
    if sum(royals) >= 5:
      score = "Full House"
    if sum(royals) >= 5 and 5 in suit_totals:
      score = "Royal Flush"
    print(score, end ="       ")

  def calculate_score(self, player):
    score = 0
    values = []
    royals = [0,0,0,0]
    suit_totals = [0,0,0,0]
    streak = 0
    straight = 0
    for v in range(0,12):
      values.append(0)
    for x in range(0,52):
      if self.drawn[x] == player:
        value = index_to_value(x)
        suit = index_to_suit(x)
        values[value - 1] += 1
        suit_totals[suit - 1] += 1
        if value == 11:
          royals[1] += 1
        if value == 12:
          royals[2] += 1
        if value == 0:
          royals[3] +=1
        if value == 1:
          royals[0] += 1
    for s in range(0,12):
      if values[s] > 0:
        streak += 1
      if values[s] <= 0:
        streak = 0
      if streak >= 5:
        straight = 1
    if sum(values[10:]) > 0:
      score = 1
    if 2 in values:
      score = 2
    if 3 in values:
      score = 3
    if values.count(2) == 2:
      score = 4
    if values.count(2) == 3:
      score = 5
    if 5 in suit_totals:
      score = 6
    if straight >= 1:
      score = 7
    if 5 in suit_totals and straight >=1:
      score = 8
    if sum(royals) >= 5:
      score = 9
    if sum(royals) >= 5 and 5 in suit_totals:
      score = 10
    return score
        

  def show_table(self, player):
    burn_prompt = "Burn a stack card into hand"
    if self.phase == "Draw Phase":
      if self.winner != "None" and self.winner != "Draw":
        print("winner is: " + self.winner + "!")
        print("")
        print("")
      if self.winner == "Draw":
        print("Draw! Split pot!")
        self.show_owner(player)
        self.show_owner("opponent")
        print("")
        print("")
      burn_prompt = "Bet a card from stack"
    if self.phase == "Show Phase":
      burn_prompt = "To Fold "
    if self.phase == "Bet Phase":
      burn_prompt = "Burn a stack card into the pot"
    self.show_stacks("opponent\'s stack")
    if self.phase == "Draw Phase":
        self.show_owner(self.winner)
        self.show_score(self.winner)
    else:
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
      print("Enter F: " + burn_prompt)
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

  def winlose(self, player, opponent):
    winner = "None"
    player_score = self.calculate_score(player)
    opp_score = self.calculate_score(opponent)
    if player_score > opp_score:
      winner = player
    elif player_score < opp_score:
      winner = opponent
    else:
      self.winner = "Draw"
      alternate = player
      for y in range(0,52):
        if self.drawn[y] == "Pot":
          self.give(y,alternate + "\'s stack")
          if alternate == player:
            alternate = opponent
          else:
            alternate =player
    self.winner = winner
    for x in range(0,52):
      if self.drawn[x] == "Pot":
        self.give(x, winner + "\'s stack")
    if self.find_next_index(player + "\'s stack",0) == -1:
      self.draw_n_times(player + "\'s stack",3)
    if self.find_next_index(opponent + "\'s stack",0) == -1:
      self.draw_n_times(opponent + "\'s stack",3)
  
  def clear_screen(self):
    for x in range(60):
      print("")
  
  def next_phase(self):
    self.phase = PHASES[((PHASES.index(self.phase) + 1) % len(PHASES))]
    
  def menu(self, selection, player):
    self.clear_screen()
    self.show_table(player)
    prompt = "Enter a number to swap/select: "
    if self.phase == "Draw Phase":
      prompt = "Enter a number to call and deal again: "
    if self.phase == "Bet Phase":
      prompt = "Select a card to use as betting chip: "
    if selection == 0:
      select = input(prompt)
      if self.phase == "Draw Phase":
        self.shuffle(player)
        self.shuffle("opponent")
        self.draw_n_times(player,5)
        self.draw_n_times("opponent",5)
        self.give(self.find_next("opponent\'s stack"), "Pot")
        self.give(self.find_next(player + "\'s stack"), "Pot")
        self.next_phase()
        self.menu(0,player)
      if select in SPECIAL_INPUT:
        return self.menu(select, player)
      return self.menu(int(select), player)
    elif selection == self.find_num_owner(player) + 1:
      if self.phase == "Draw Phase":
        self.shuffle(player)
        self.shuffle("opponent")
        self.draw_n_times(player,5)
        self.draw_n_times("opponent",5)
        self.give(self.find_next("opponent\'s stack"), "Pot")
        self.give(self.find_next(player + "\'s stack"), "Pot")
        self.next_phase()
        self.menu(0,player)
      if self.phase == "Show Phase":
        self.winlose("folded", "opponent")
        self.next_phase()
        return self.menu(0, player)
      elif self.phase == "Bet Phase":
        self.give(self.find_next(player + "\'s stack"), "Pot")
        return self.menu(0,player)
      self.give(self.find_next(player + "\'s stack"), player)
      return self.menu(0, player)
    elif selection == 'P' or selection == 'p':
      if self.phase == "Draw Phase":
        self.shuffle(player)
        self.shuffle("opponent")
        self.draw_n_times(player,5)
        self.draw_n_times("opponent",5)
        self.give(self.find_next("opponent\'s stack"), "Pot")
        self.give(self.find_next(player + "\'s stack"), "Pot")
        self.next_phase()
        self.menu(0,player)
      if self.phase == "Show Phase":
        self.winlose(player, "opponent")
        self.next_phase()
        return self.menu(0, player)
      else:
        self.next_phase()
        self.menu(0,player)
    elif selection == 'f' or selection == 'F' and self.phase == "Show Phase":
      self.winlose("folded", "opponent")
      self.next_phase()
      return self.menu(0, player)
    else:
      if self.swaps >= 2:
        self.next_phase()
        self.swaps = 0
        self.menu(0, player)
      if self.phase == "Draw Phase":
        self.shuffle(player)
        self.shuffle("opponent")
        self.draw_n_times(player,5)
        self.draw_n_times("opponent",5)
        self.give(self.find_next("opponent\'s stack"), "Pot")
        self.give(self.find_next(player + "\'s stack"), "Pot")
        self.next_phase()
        self.menu(0,player)
      if self.phase == "Show Phase":
        self.winlose(player, "opponent")
        self.next_phase()
        return self.menu(0, player)
      elif self.phase == "Bet Phase":
        self.give(self.find_next_index(player, int(selection)),"Pot")
        return self.menu(0, player)
      self.give(self.find_next_index(player, int(selection)), "Discard")
      self.draw(player)
      self.swaps += 1
      return self.menu(0, player)
      
  def start_game(self, player, opponent):
    self.draw_n_times(player,5)
    self.draw_n_times(opponent,5)
    self.draw_n_times(player + "\'s stack", 3)
    self.draw_n_times(opponent + "\'s stack", 3)
    self.draw_n_times("Pot",2)
    self.menu(0, player)


if __name__ == "__main__":
  test_deck = deck()
  test_deck.start_game("me","opponent")
  
