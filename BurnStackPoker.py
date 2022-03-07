import random

DISCARD_PILE = "Discard"
DECK = "Deck"
PLAYING = "Playing"
FOLDED = "Folded"
BANKRUPT = "Bankrupt"


class Table:
    def __init__(self, players):
        self.pot = []
        self.deck = Deck()
        self.players = players
        self.winner = Player("nobody", self.pot, self.deck)
        self.winnerRank = 10
        self.call = 1


    def check_winner(self, player):
        player.hand.calculate_rank()
        if player.hand.rank < self.winnerRank:
            self.winner = player
            self.winnerRank = player.hand.rank
            print(self.winner.name + " Wins!")

    def reward_winner(self):
        for card in self.pot:
            self.winner.enstack(card)

    def show_turn(self, player):
        print("--" + player.name + "s turn--")
        print("\tcurrent pot: " + str(len(self.pot)) + " card(s)")
        print("\tcurrent bets: " + str(player.current_bet) + " card(s)")
        print("\tyour stack: " + str(len(player.hand.stack)) + " card(s)")

    def start_game(self):
        while True:
            self.call = 1
            for player in self.players:
                player.unfold()
                self.deck.deal(player, 5)
                self.deck.deal_stack(player, 5)
            # start betting
            for player in self.players:
                self.show_turn(player)
                player.call_phase(self.call)
            # bet phase
            for player in self.players:
                self.show_turn(player)
                self.call = player.bet_phase()
            # swap phase
            for player in self.players:
                self.show_turn(player)
                player.swap_phase()
            # bet/burn phase
            for player in self.players:
                self.show_turn(player)
                new_call = player.bet_or_burn_phase(self.call)
                if self.call < new_call:
                    self.call = new_call
            # compare phase
            for player in self.players:
                player.hand.calculate_rank()
                self.check_winner(player)
                self.winner.hand.show()
            # reward phase
            self.reward_winner()

            for player in self.players:
                player.discard_phase()


class Player:
    def __init__(self, name, pot, deck):
        self.name = name
        self.hand = Hand(name)
        self.pot = pot
        self.deck = deck
        self.current_bet = 0
        self.state = PLAYING

    def prompt(self, msg):
        answer = input(msg + " Y/n?: ")
        if answer == "n" or answer == "N":
            return False
        else:
            return True

    def unfold(self):
        if self.state != PLAYING:
            print(self.name + " is ready to play")
            self.state = PLAYING

    def fold(self):
        print(self.name + " Folded")
        self.state = FOLDED

    def hand_prompt(self, msg):
        selected = []
        self.hand.show()
        print(msg)
        selection = input("Pick a card by integer index, -1 to not swap: ")
        if int(selection) >= 0:
            selected.append(int(selection))
        second_selection = input("Pick a second card by integer index, -1 to not swap: ")
        if int(second_selection) >= 0 >= selection.count(second_selection):
            selected.append(int(second_selection))
        return selected

    def prompt_amount(self):
        return int(input("Input amount as an Integer: "))

    def draw(self, card):
        self.hand.draw(card)

    def burn(self, amount):
        self.hand.burn(amount)

    def enstack(self, cards):
        self.hand.enstack(cards)

    def bet_stack(self, amount):
        to_be_bet = self.bet(amount)
        self.current_bet += amount
        for card in to_be_bet:
            self.pot.append(card)

    def call_phase(self, quantity):
        if self.state != PLAYING:
            return self.current_bet
        if self.prompt("Call to " + str(quantity) + "? ") and self.current_bet < quantity:
            self.bet(quantity - self.current_bet)
        elif self.current_bet > quantity:
            print("already called")
        else:
            self.fold()

    def swap(self, index):
        self.hand.discard(index)
        self.deck.deal(self)

    def discard_phase(self):
        self.current_bet = 0
        while len(self.hand.cards) > 0:
            self.deck.shuffle(self.hand.cards.pop())

    def swap_phase(self):
        if self.state != PLAYING:
            return
        if self.prompt("Swap up to two cards"):
            to_replace = self.hand_prompt("Choose swapped cards")
            for replacement in to_replace:
                self.swap(replacement)
        self.show()

    def bet_phase(self):
        if self.state != PLAYING:
            return self.current_bet
        if self.prompt("bet from stack"):
            amount = self.prompt_amount()
            self.hand.bet(amount)
        return self.current_bet

    def bet_or_burn_phase(self, quantity):
        if self.state != PLAYING:
            return self.current_bet
        if self.prompt("burn from stack into hand"):
            amount = self.prompt_amount()
            self.burn(amount)
            self.show()
        self.bet_phase()
        return self.current_bet

    def bet(self, amount=1):
        return self.hand.bet(amount)

    def show(self):
        self.hand.show()


class Hand:
    HAND_NAMES = ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight",
                  "Three of a Kind", "Two Pair", "One Pair", "High Card"]

    def __init__(self, player_name):
        self.cards = []
        self.stack = []
        self.royal = False
        self.flush = False
        self.straight = False
        self.has_high = False
        self.name = self.HAND_NAMES[9]
        self.pairs = 0
        self.kind = 0
        self.rank = 9
        self.player_name = player_name

    def discard(self, index):
        to_be_discarded = self.cards.pop(index)
        to_be_discarded.discard()

    def bet(self, amount=1):
        if amount > len(self.stack):
            print("Out of Stack")
            return
        selected_cards = []
        for times in range(amount):
            betted_card = self.stack.pop()
            betted_card.bet()
            selected_cards.append(betted_card)
        return selected_cards

    def draw(self, card):
        self.cards.append(card)

    def enstack(self, cards):
        for card in cards:
            self.stack.append(card)

    def burn(self, num_times=1):
        if len(self.stack) < num_times:
            return
        else:
            for times in range(num_times):
                burnt_card = self.stack.pop()
                burnt_card.draw(self.name)
                self.draw(burnt_card)

    def show(self):
        self.calculate_rank()
        text = ""
        for card in self.cards:
            text += card.card_form()
        print(self.player_name)
        print(text)
        print(self.name)
        print("Stack remaining: " + str(len(self.stack)))

    def __hand_to_vals__(self):
        vals = []
        for card in self.cards:
            vals.append(card.value)
        return vals

    def compare(self, hand):
        return self.rank - hand.rank

    def calculate_rank(self):
        self.has_kind()
        self.is_royal()
        self.is_straight()
        self.is_high()
        if self.royal and self.flush and self.straight:
            self.rank = 1
        elif self.straight and self.flush:
            self.rank = 2
        elif self.kind >= 4:
            self.rank = 3
        elif self.royal:
            self.rank = 4
        elif self.flush:
            self.rank = 5
        elif self.straight:
            self.rank = 6
        elif self.kind == 3:
            self.rank = 7
        elif self.pairs >= 2:
            self.rank = 8
        elif self.kind == 2:
            self.rank = 9
        elif self.has_high:
            self.rank = 10
        self.name = self.HAND_NAMES[self.rank - 1]

    def is_royal(self):
        self.royal = True
        for card in self.cards:
            if not card.face:
                self.royal = False

    def is_flush(self):
        self.flush = True
        suit = self.cards[0].suit
        for card in self.cards:
            if card.suit != suit:
                self.flush = False

    def is_straight(self):
        if len(self.cards) < 5 or not self.kind <= 1:
            self.straight = False
            return
        in_row = 1
        values = self.__hand_to_vals__()
        current = min(values)
        while len(values) > 0:
            current = min(values)
            if in_row >= 5:
                self.straight = True
                return
            else:
                values.remove(current)
                next = min(values)
                if next == current + 1:
                    in_row += 1
                    current = next
                elif in_row < 5:
                    self.straight = False
                    return

    def is_high(self):
        self.has_high = False
        for card in self.cards:
            if card.face:
                self.has_high = True

    def has_kind(self):
        top_kind = 0
        self.pairs = 0
        self.kind = 0
        kind = 0
        types = []
        for card in self.cards:
            if top_kind < kind:
                top_kind = kind
            kind = 0
            for comp_card in self.cards:
                if kind >= 2:

                    if types.count(card.value) <= 0:
                        if len(types) > 0:
                            self.pairs += 1

                        types.append(card.value)
                if comp_card.value == card.value:
                    kind += 1
        self.kind = top_kind


class Deck:
    NUMBER_OF_CARDS = 52
    NUMBER_OF_SUITS = 4
    POT = "Pot"

    def __init__(self):
        self.cards = []
        for cardIndex in range(1, self.NUMBER_OF_CARDS):
            # A bit ridiculous looking, but a modulo can find the suit and division can find value if in order of suit
            self.cards.append(Card(cardIndex % self.NUMBER_OF_SUITS, round(cardIndex / self.NUMBER_OF_SUITS)))

    def __in_deck__(self):
        selection = filter(lambda x: not x.discarded and not x.drawn and not x.enstacked, self.cards)
        return list(selection)

    def shuffle(self, card):
        card.drawn = False
        card.betted = False
        card.enstacked = False
        card.discarded = False
        self.cards.append(card)

    def deal(self, player, num_times=1):
        for times in range(num_times):
            #TODO this doesn't work
            selected_card = random.choice(self.cards)
            player.draw(selected_card)
            self.cards.remove(selected_card)

    def deal_stack(self, player, num_times=1):
        for times in range(num_times):
            # TODO this doesn't work
            selected_card = random.choice(self.cards)
            player.enstack([selected_card])
            self.cards.remove(selected_card)

    def enstack(self, player, num_times=1):
        selected = []
        for times in range(num_times):
            selection = self.__in_deck__()
            selected_card = random.choice(selection)
            selected_card.enstack(player)
            selected.append(selected_card)


class Card:
    SUITS = {0: "♠", 1: "♣", 2: "♦", 3: "♥"}
    FACES = {0: "A", 1: "J", 2: "Q", 3: "K"}
    POT = "Pot"

    def __init__(self, suit, value):
        self.suit = self.SUITS[suit]
        self.value = value
        self.face = True if self.value > 10 else False
        self.printed = self.suit + str(self.value) if not self.face else self.suit + str(self.FACES[value - 11])
        self.owner = DECK
        self.discarded = False
        self.drawn = False
        self.enstacked = False
        self.betted = False

    def card_form(self):
        return "[" + self.printed + "]"

    def show(self):
        print(self.card_form())

    def draw(self, player):
        self.drawn = True
        self.enstacked = False
        self.owner = player

    def enstack(self, player):
        self.enstacked = True
        self.drawn = False
        self.owner = player

    def discard(self):
        self.owner = DISCARD_PILE
        self.discarded = True

    def bet(self):
        self.betted = True
        self.owner = self.POT

    def shuffle(self):
        self.owner = DECK
        self.drawn = False
        self.discarded = False

if __name__ == "__main__":
    test_table = Table([])
    test_player = Player("dave",test_table.pot,test_table.deck)
    test_player_2 = Player("not dave",test_table.pot,test_table.deck)
    test_table.players.append(test_player)
    test_table.players.append(test_player_2)
    test_table.start_game()
