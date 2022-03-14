import math
import random

DISCARD_PILE = "Discard"
DECK = "Deck"
POT = "Pot"
PLAYING = "Playing"
FOLDED = "Folded"
BANKRUPT = "Bankrupt"


class Table:
    def __init__(self, players):
        self.pot = []
        self.deck = Deck()
        self.players = players
        self.winner = Player("nobody")
        self.winnerRank = 10
        self.call = 1

    def add_player(self, player):
        player.pot = self.pot
        player.deck = self.deck
        self.players.append(player)

    def check_winner(self, player):
        player.hand.calculate_rank()
        if player.hand.rank <= self.winnerRank:
            self.winner = player
            self.winnerRank = player.hand.rank
            print(self.winner.name + " Wins!")

    def reward_winner(self):
        pot_list = []
        while len(self.pot) > 0:
            pot_list.append(self.pot.pop())
        self.winner.add_to_stack(pot_list)

    def show_turn(self, player):
        print("--" + player.name + "s turn--")
        print("\tcurrent pot: " + str(len(self.pot)) + " card(s)")
        print("\tcurrent bets: " + str(player.current_bet) + " card(s)")
        print("\tyour stack: " + str(len(player.hand.stack)) + " card(s)")
        player.hand.show()

    def start_game(self):
        for player in self.players:
            self.deck.deal_stack(player, 5)
        while True:
            self.call = 1
            for player in self.players:
                if player.state == BANKRUPT:
                    self.deck.deal_stack(player, 5)
                player.unfold()
                self.deck.deal(player, 5)
            # start betting
            for player in self.players:
                self.show_turn(player)
                player.call_phase(self.call)
            # bet phase
            for player in self.players:
                self.show_turn(player)
                new_call = player.bet_phase()
                if self.call < new_call:
                    self.call = new_call
                    for player_called in self.players:
                        self.show_turn(player_called)
                        player_called.call_phase(self.call)
            # swap phase
            for player in self.players:
                self.show_turn(player)
                player.swap_phase()
            # bet/burn phase
            for player in self.players:
                self.show_turn(player)
                new_call = player.bet_or_burn_phase()
                if self.call < new_call:
                    self.call = new_call
                    for player_called in self.players:
                        self.show_turn(player_called)
                        player_called.call_phase(self.call)
            # compare phase
            for player in self.players:
                if len(player.hand.stack) <= 0:
                    player.state = BANKRUPT
                    print(player.name + " is bankrupt!")
                player.hand.calculate_rank()
                self.check_winner(player)
                self.winner.hand.show()
            # reward phase
            self.reward_winner()
            for player in self.players:
                player.discard_phase()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand(name)
        self.pot = []
        self.deck = Deck()
        self.current_bet = 0
        self.state = PLAYING

    @staticmethod
    def prompt(msg):
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

    def hand_prompt(self):
        selected = []
        self.hand.show_cards()
        selection = input("Pick a card by integer index to swap, -1 to not swap: ")
        if int(selection) >= 0:
            selected.append(int(selection))
        second_selection = input("Pick a second card by integer index, -1 to not swap: ")
        if int(second_selection) >= 0 >= selection.count(second_selection):
            selected.append(int(second_selection))
        return selected

    @staticmethod
    def prompt_amount(msg):
        return int(input("Input " + msg + " as an Integer: "))

    def draw(self, card):
        self.hand.draw(card)

    def burn(self, amount):
        self.hand.burn(amount)

    def add_to_stack(self, cards):
        self.hand.add_to_stack(cards)

    def bet_stack(self, amount):
        to_be_bet = self.bet(amount)
        self.current_bet += len(to_be_bet)
        for card in to_be_bet:
            self.pot.append(card)

    def call_phase(self, quantity):
        if self.state != PLAYING:
            return self.current_bet
        if self.current_bet < quantity:
            if self.prompt("Call to " + str(quantity) + "? ") and self.current_bet < quantity:
                self.bet_stack(quantity - self.current_bet)
            else:
                self.fold()

    def swap(self, index):
        self.deck.shuffle(self.hand.cards.pop(index))
        self.deck.deal(self)

    def discard_phase(self):
        self.current_bet = 0
        while len(self.hand.cards) > 0:
            self.deck.shuffle(self.hand.cards.pop())

    def swap_phase(self):
        if self.state != PLAYING:
            return
        to_replace = self.hand_prompt()
        for replacement in to_replace:
            self.swap(replacement)

    def bet_phase(self):
        if self.state != PLAYING:
            return self.current_bet
        amount = self.prompt_amount("bet (0 to not bet)")
        if amount > 0:
            self.bet_stack(amount)
        return self.current_bet

    def bet_or_burn_phase(self):
        if self.state != PLAYING:
            return self.current_bet
        amount = self.prompt_amount("burn cards from stack (0 to not burn)")
        if amount > 0:
            self.burn(amount)
        self.bet_phase()
        return self.current_bet

    def bet(self, amount=1):
        return self.hand.bet(amount)

    def show(self):
        self.hand.show()

    def show_unicode(self):
        self.hand.show_unicode()


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

    def bet(self, amount=1):
        if amount > len(self.stack):
            print("Out of Stack")
            return []
        selected_cards = []
        for times in range(amount):
            bet_card = self.stack.pop()
            bet_card.bet()
            selected_cards.append(bet_card)
        return selected_cards

    def draw(self, card):
        self.cards.append(card)

    def add_to_stack(self, cards):
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
        print("\t" + self.player_name + "\'s hand:")
        print("\t" + text)
        print("\t" + self.name)

    def show_unicode(self):
        self.calculate_rank()
        text = ""
        for card in self.cards:
            text += card.unicode
        return text

    def show_string(self):
        self.calculate_rank()
        text = ""
        for card in self.cards:
            text += card.card_form()
        return text

    def show_cards(self):
        self.calculate_rank()
        text = ""
        under_text = ""
        index = 0
        for card in self.cards:
            text += card.card_form()
            under_text += "\t" + str(index)
            index += 1
        print("\t" + text)
        print(under_text)

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
        elif self.kind >= 3 and self.pairs >= 1:
            # full house changed
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
        while len(values) > 0:
            current = min(values)
            if in_row >= 5:
                self.straight = True
                return
            else:
                values.remove(current)
                next_in_row = min(values)
                if next_in_row == current + 1:
                    in_row += 1
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
    CARDS_PER_SUIT = 14

    def __init__(self):
        self.cards = []
        for cardIndex in range(1, self.NUMBER_OF_CARDS + 4):
            # A bit ridiculous looking, but a modulo can find the suit and division can find value if in order of suit
            card_suit = math.floor(cardIndex / self.CARDS_PER_SUIT)
            card_val = cardIndex % self.CARDS_PER_SUIT
            if card_val == 1 or card_val == 0 and card_suit == 0 :
                continue
            self.cards.append(Card(card_suit,card_val))

    def __in_deck__(self):
        selection = filter(lambda x: not x.discarded and not x.drawn and not x.in_stack, self.cards)
        return list(selection)

    def shuffle(self, card):
        card.drawn = False
        card.in_pot = False
        card.in_stack = False
        card.discarded = False
        self.cards.append(card)

    def deal(self, player, num_times=1):
        for times in range(num_times):
            selected_card = random.choice(self.cards)
            player.draw(selected_card)
            self.cards.remove(selected_card)

    def deal_stack(self, player, num_times=1):
        for times in range(num_times):
            selected_card = random.choice(self.cards)
            player.add_to_stack([selected_card])
            self.cards.remove(selected_card)

    def add_to_stack(self, player, num_times=1):
        selected = []
        for times in range(num_times):
            selection = self.__in_deck__()
            selected_card = random.choice(selection)
            selected_card.enstack(player)
            selected.append(selected_card)


class Card:
    SUITS = {0: "♠", 1: "♣", 2: "♦", 3: "♥"}
    FACES = {0: "A", 1: "J", 2: "Q", 3: "K"}
    UNICODES_SPADES = ["","🂢", "🂣", "🂤", "🂥", "🂦", "🂧", "🂨", "🂩", "🂪", "🂡", "🂫", "🂭", "🂮"]
    UNICODES_CLUBS = ["","🃒", "🃓", "🃔", "🃕",
                "🃖", "🃗", "🃘", "🃙", "🃚", "🃑", "🃛", "🃝", "🃞"]

    UNICODES_DIAMONDS =["","🃂", "🃃", "🃄", "🃅", "🃆", "🃇", "🃈", "🃉",
                "🃊", "🃁", "🃋", "🃍", "🃎"]
    UNICODES_HEARTS = ["","🂲", "🂳", "🂴", "🂵", "🂶", "🂷", "🂸", "🂹", "🂺", "🂱", "🂻", "🂽",
                "🂾"]

    def __init__(self, suit, value):
        self.suit = self.SUITS[suit]
        self.suit_num = suit
        self.value = value
        self.face = True if self.value > 10 else False
        self.printed = self.suit + str(self.value) if not self.face else self.suit + str(self.FACES[value - 11])
        self.owner = DECK
        self.discarded = False
        self.drawn = False
        self.in_stack = False
        self.in_pot = False
        if self.suit_num == 0:
            self.unicode = self.UNICODES_SPADES[self.value - 1]
        elif self.suit_num == 1:
            self.unicode = self.UNICODES_CLUBS[self.value - 1]
        elif self.suit_num == 2:
            self.unicode = self.UNICODES_DIAMONDS[self.value - 1]
        else:
            self.unicode = self.UNICODES_HEARTS[self.value - 1]



    def card_form(self):
        return "[" + self.printed + "]"

    def show(self):
        print(self.card_form())

    def draw(self, player):
        self.drawn = True
        self.in_stack = False
        self.owner = player

    def enstack(self, player):
        self.in_stack = True
        self.drawn = False
        self.owner = player

    def discard(self):
        self.owner = DISCARD_PILE
        self.discarded = True

    def bet(self):
        self.in_pot = True
        self.owner = POT

    def shuffle(self):
        self.owner = DECK
        self.drawn = False
        self.discarded = False


if __name__ == "__main__":
    test_table = Table([])
    test_player = Player("dave")
    test_player_2 = Player("not dave")
    test_table.add_player(test_player)
    test_table.add_player(test_player_2)
    test_table.start_game()