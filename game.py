import random as rand
SUITS = "♥♦♠♣"
VALUES = "123456789JQK"

def index_to_card(index):
  suit = SUITS[round((index + 1) / 12) - 1]
  value = VALUES[((index + 1) % 4) - 1]
  return "[" + suit + value + "]"

class deck:
  def __init__(self):
    self.drawn = [];
    self.decksize = 52;
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
    self.drawn[index] = new_owner
    
  def shuffle(self, from_owner):
    for x in range(0,52):
      if(self.drawn[x] == from_owner or from_owner == "All" and self.drawn[x] != "Dealer"):
        self.drawn[x] = "Dealer"
        self.decksize+=1

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
    stack_size = 0
    for x in range(0,52):
      if self.drawn[x] == owner:
        stack_size +=1
        
    ten_stacks = round(stack_size / 10)
    without_tens = ten_stacks % 10
    if stack_size < 10:
      without_tens = stack_size
    for w in range(1, without_tens):
      print("[", end='')
    if stack_size >= 1:
      print("[" +converted + ":" + str(stack_size) + "]", end='')
    print("")


  def show_table(self, player):
    self.show_stacks("opponent\'s stack")
    self.show_owner_hidden("opponent")
    print("")
    self.show_stacks("Dealer")
    print("")
    print("")
    self.show_owner(player)
    print("  1    2    3    4    5    6: Burn a card into hand")
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
        current+=1
        if current == index:
          return x
    return -1

  def menu(self, selection, player):
    if selection == 0:
      self.show_table(player)
      select = input("Enter a number to select: ")
      return self.menu(select, player)
    elif selection == 6:
      self.give(self.find_next_index(player + "\'s stack",1,), player)
      return self.menu(0, player)
    else:
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
  
