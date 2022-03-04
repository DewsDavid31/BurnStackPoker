import random


class Player:
    # Default size of stack for a player is 5 for now
    # unless player number in a match or deflation of pots get out of hand.
    def __init__(self, name, table):
        self.name = name
        self.hand = []
        self.table = table
        self.stack = Stack(table.stack_size, self.table.deck)
        self.state = "Playing"

    def show(self):
        # For now, shows players name then each card in their hand in current drawn order
        print(self.name)
        if len(self.stack.cards) <= 0:
            print("Bankrupt, out of cards")
            self.state = "Bankrupt"
        else:
            handstring = ""
            for card in self.hand:
                handstring += card.string()
            print(handstring)
            print("your stack remaining: " + str(len(self.stack.cards)))

    def play_hand(self):
        #TODO: behavior might not be as intended
        copy = self.hand[:]
        self.hand.clear()
        return copy

    def draw(self, quantity=1):
        print("drawing  " + str(quantity) + " card(s)")
        drawn_cards = self.table.deck.deal(quantity)
        for card in drawn_cards:
            self.hand.append(card)

    def take_turn(self):
        # used wrong python version for match
        self.show()
        option = input("-your turn- : ")
        if option == "burn":
            burnt_cards = self.stack.burn()
            print("Burned into hand:")
            for card in burnt_cards:
                card.show()
                self.hand.append(card)
        elif option == "bet":
            self.table.bet(self.stack.burn())
        elif option == "play":
            self.play_hand()
            self.state = "Passing"
        else:
            print("Not an option")
class Deck:
    NUMBER_OF_CARDS = 52
    NUMBER_OF_SUITS = 4
    def __init__(self):
        self.cards = []
        for cardIndex in range(1,self.NUMBER_OF_CARDS):
            # A bit ridiculous looking, but a modulo can find the suit and division can find value if in order of suit
                self.cards.append(Card(cardIndex % self.NUMBER_OF_SUITS, round(cardIndex / self.NUMBER_OF_SUITS)))

    def deal(self, num_times=1):
        # shuffling is avoided by selecting and drawing a card at random from the deck
        selected = 0
        selected_cards = []
        while(selected < num_times):
            picked = random.randint(0,len(self.cards) - 1)
            selected_cards.append(self.cards.pop(picked))
            selected += 1
        return selected_cards


    def shuffle(self, cards):
        for card in cards:
            self.cards.append(card)

class Card:
    SUITS = {0:"♠",1:"♣",2:"♦",3:"♥"}
    FACES = {0:"A",1:"J",2:"Q",3:"K"}
    def __init__(self,suit,value):
        self.suit = self.SUITS[suit]
        self.value = value

    def show(self):
        if self.value > 10:
            print("[" + str(self.suit) + "" + str(self.FACES[self.value - 11]) + "]")

        else:
            print("[" + str(self.suit) + "" + str(self.value) + "]")

    def string(self):
        if self.value > 10:
            return "[" + str(self.suit) + "" + str(self.FACES[self.value - 11]) + "]"

        else:
            return "[" + str(self.suit) + "" + str(self.value) + "]"

class Stack:

    def __init__(self, size, deck):
        self.cards = []
        self.size = size
        self.deck = deck
        drawn_cards = deck.deal(size)
        for card in drawn_cards:
            self.cards.append(card)

    def gain(self, cards):
        for card in cards:
            self.cards.append(card)

    def reset(self):
        self.cards = []
        drawn_cards = self.deck.deal(self.size)
        for card in drawn_cards:
            self.cards.append(card)

    def burn(self, num_times=1):
        selected = 0
        selected_cards = []
        if len(self.cards) <= 1:
            return [self.cards.pop()]
        while (selected < num_times):
            picked = random.randint(0, len(self.cards) - 1)
            selected_cards.append(self.cards.pop(picked))
            selected += 1
        return selected_cards


class Table:

    def __init__(self, stack_size=5):
        self.pot = []
        self.cards = []
        self.players = []
        self.deck = Deck()
        self.stack_size = stack_size
        self.state = "open"

    def add_player(self, name):
        added_player = Player(name, self)
        self.players.append(added_player)

    def bet(self, card):
        self.pot.append(card)
        print("-A stack card was bet-")
        print("Current pot: " + str(len(self.pot)))

    def clear_pot(self):
        while(len(self.pot) > 0):
            reshuffled_card = self.pot.pop()
            self.deck.shuffle(reshuffled_card)


    def start_game(self):
        while(self.state != "closed"):
            for player_dealt in self.players:
                print("Dealing stacks and hands...")
                self.clear_pot()
                self.deck.shuffle(player_dealt.play_hand())
                player_dealt.state = "Ready"
                player_dealt.draw(5)
                player_dealt.stack.reset()
            passing_players = 0
            while(passing_players < len(self.players)):
                for player_turn in self.players:
                    if player_turn.state != "Passing" and player_turn.state != "Bankrupt":
                        player_turn.take_turn()
                        player_turn.show()
                    else:
                        passing_players += 1

if __name__ == "__main__":
    test_table = Table()
    test_table.add_player("you")
    test_table.start_game()

#Non-MVC portion

class model:
    pass

class view:
    pass

class control:
    pass