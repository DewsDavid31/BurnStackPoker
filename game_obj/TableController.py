# MVC Version of our game file with state-based actions so SQL can hold poker tables

# State-Machine
# e -draw> s1 -Fold/Bankrupt> s3
#  s1 -Bet> s1
# s1 -Call> s2
# s2 -Bet/Burn/swap> s2
# s2 -Fold/Bankrupt> s3
# s2 -Call> s4
# s4 -DiscardDeal> s1
import math
import random
import uuid

STATE_TABLE = [[0, 0, 1, 3], [1, 1, 2, 3], [2, 2, 3, 3], [0, 0, 0, 0]]
STATES = ["Bet Phase", "Bet Burn and Swap Phase", "Folded", "Show Cards Phase"]
OPTIONS = ["Bet", "Burn", "Pass", "Fold"]


class TableController:
    #TODO: players are not singleton yet
    #TODO: everyone sees same player
    def __init__(self):
        self.option = 0
        self.state = STATE_TABLE[0][0]
        self.players = []
        self.player_names = []
        self.you = Player("Player #" + str(uuid.UUID.int))

    def get_player_hands(self):
        hands = ""
        for player in self.players:
            hands +=  "," + player.hand.show_unicode()
        return hands

    def get_player_stacks(self):
        stacks = ""
        for player in self.players:
            stacks += "," + player.hand.show_stack_unicode()
        return stacks

    def get_state(self):
        return STATES[self.state]

    def get_names(self):
        return self.player_names

    def add_player(self, player_name):
        new_player = Player(player_name)
        self.player_names.append(new_player)
        self.players.append(new_player)

    def load_player(self, player_name, hand, stack):
        new_player = Player(player_name)
        new_player.hand.load_unicode(hand)
        new_player.hand.load_stack_unicode(stack)
        self.players.append(new_player)
        self.player_names.append(player_name)

    def kick_player(self, player_name):
        self.player_names.remove(player_name)
        self.players.remove(lambda x: x.name == player_name)

    def load_state(self, state, user_name, user_hand, user_stack, player_names, player_hands, player_stacks):
        self.state = state
        self.you.name = user_name
        self.you.stack = user_stack
        self.you.hand.load_unicode(user_hand)
        player_names_split = player_names.split(",")
        player_hands_split = player_hands.split(",")
        player_stacks_split = player_stacks.split(",")

        if len(player_names_split) != len(player_hands_split) != len(player_stacks_split):
            print("Error! Invalid state data, table corrupted!")
            return
            # TODO: need better error handling here
        if len(player_names) < 1:
            return
        elif len(player_hands) < 1 and len(player_stacks) < 1:
            for index in range(len(player_names) - 1):
                self.load_player(player_names_split[index], "", "")
        elif len(player_hands) < 1:
            for index in range(len(player_names) - 1):
                self.load_player(player_names_split[index], "", player_stacks_split[index])
        elif len(player_stacks) < 1:
            for index in range(len(player_names) - 1):
                self.load_player(player_names_split[index], player_hands_split[index], "")
        else:
            for index in range(len(player_names) - 1):
                self.load_player(player_names_split[index], player_hands_split[index], player_stacks_split[index])

    def save_state(self):
        names = ""
        hands = ""
        stacks = ""
        for player in self.players:
            names += player.name
            hands += player.hand.show_unicode()
            stacks += player.hand.show_stack_unicode()
        return self.state, self.you.name, self.you.hand.show_unicode(), self.you.hand.show_stack_unicode(), names, hands, stacks

    def do_action(self, option):
        if option == 0:
            self.you.deck.deal(self.you,5)
            self.you.deck.deal_stack(self.you,5)
            self.you.bet()
        elif option == 1:
            self.you.burn(1)
        elif option == 2:
            #TODO: swapping is difficult in this ui, only swaps first card for now
            self.you.swap(0)
        elif option == 3:
            return
        else:
            print("Error!: Invalid option on state machine")

    def change_state(self, option):
        self.state = STATE_TABLE[self.state][option]
        self.do_action(option)

    def bet_button(self):
        self.change_state(0)

    def burn_button(self):
        self.change_state(1)

    def fold_button(self):
        self.change_state(3)

    def pass_button(self):
        self.change_state(2)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand(name)
        self.pot = []
        self.deck = Deck()
        self.current_bet = 0

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

    def swap(self, index):
        self.deck.shuffle(self.hand.cards.pop(index))
        self.deck.deal(self)

    def discard_phase(self):
        self.current_bet = 0
        while len(self.hand.cards) > 0:
            self.deck.shuffle(self.hand.cards.pop())

    def bet(self, amount=1):
        return self.hand.bet(amount)


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

    def card_values(self):
        vals = []
        for card in self.cards:
            vals.append(card.value)
        return vals

    def card_suits(self):
        suits = []
        for card in self.cards:
            suits.append(card.suit_num)
        return suits

    def load_stack_unicode(self, unicode):
        self.stack = []
        for code in unicode:
            if code in Card.UNICODES_DIAMONDS:
                index = Card.UNICODES_DIAMONDS.index(code)
                self.stack.append(Card(2, index))

            elif code in Card.UNICODES_CLUBS:
                index = Card.UNICODES_CLUBS.index(code)
                self.stack.append(Card(1, index))

            elif code in Card.UNICODES_SPADES:
                index = Card.UNICODES_SPADES.index(code)
                self.stack.append(Card(0, index))
            else:
                index = Card.UNICODES_HEARTS.index(code)
                self.stack.append(Card(3, index))


    def load_unicode(self, unicode):
        self.cards = []
        for code in unicode:
            if code in Card.UNICODES_DIAMONDS:
                index = Card.UNICODES_DIAMONDS.index(code)
                self.cards.append(Card(2, index))

            elif code in Card.UNICODES_CLUBS:
                index = Card.UNICODES_CLUBS.index(code)
                self.cards.append(Card(1, index))

            elif code in Card.UNICODES_SPADES:
                index = Card.UNICODES_SPADES.index(code)
                self.cards.append(Card(0, index))
            else:
                index = Card.UNICODES_HEARTS.index(code)
                self.cards.append(Card(3, index))

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

    def show_unicode(self):
        self.calculate_rank()
        text = ""
        for card in self.cards:
            text += card.unicode
        return text

    def show_stack_unicode(self):
        text = ""
        for card in self.stack:
            text += card.unicode
        return text

    def show_string(self):
        self.calculate_rank()
        text = ""
        for card in self.cards:
            text += card.card_form()
        return text

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
            if card_val == 1 or card_val == 0 and card_suit == 0:
                continue
            self.cards.append(Card(card_suit, card_val))

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
    UNICODES_SPADES = ["", "🂢", "🂣", "🂤", "🂥", "🂦", "🂧", "🂨", "🂩", "🂪", "🂡", "🂫", "🂭", "🂮"]
    UNICODES_CLUBS = ["", "🃒", "🃓", "🃔", "🃕",
                      "🃖", "🃗", "🃘", "🃙", "🃚", "🃑", "🃛", "🃝", "🃞"]

    UNICODES_DIAMONDS = ["", "🃂", "🃃", "🃄", "🃅", "🃆", "🃇", "🃈", "🃉",
                         "🃊", "🃁", "🃋", "🃍", "🃎"]
    UNICODES_HEARTS = ["", "🂲", "🂳", "🂴", "🂵", "🂶", "🂷", "🂸", "🂹", "🂺", "🂱", "🂻", "🂽",
                       "🂾"]

    def __init__(self, suit, value):
        self.suit = self.SUITS[suit]
        self.suit_num = suit
        self.value = value
        self.face = True if self.value > 10 else False
        self.printed = self.suit + str(self.value) if not self.face else self.suit + str(self.FACES[value - 11])
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

    def draw(self, player):
        self.drawn = True
        self.in_stack = False

    def enstack(self, player):
        self.in_stack = True
        self.drawn = False

    def discard(self):
        self.discarded = True

    def bet(self):
        self.in_pot = True

    def shuffle(self):
        self.drawn = False
        self.discarded = False
