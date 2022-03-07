import random

DISCARD_PILE = "Discard"
DECK = "Deck"


class Hand:
    HAND_NAMES = ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "High Card"]

    def __init__(self, player_name):
        self.cards = []
        self.royal = False
        self.flush = False
        self.straight = False
        self.has_high = False
        self.name = self.HAND_NAMES[10]
        self.pairs = 0
        self.kind = 0
        self.rank = 9
        self.player_name = player_name

    def show(self):
        text = ""
        for card in self.cards:
            text += card.printed()
        print(self.player_name)
        print(text)
        print(self.name)

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
        while (len(values) > 0):
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

    def __init__(self):
        self.cards = []
        for cardIndex in range(1, self.NUMBER_OF_CARDS):
            # A bit ridiculous looking, but a modulo can find the suit and division can find value if in order of suit
            self.cards.append(Card(cardIndex % self.NUMBER_OF_SUITS, round(cardIndex / self.NUMBER_OF_SUITS)))

    def __in_deck__(self):
        selection = filter(lambda x: not x.discarded and not x.drawn, self.cards)
        return list(filter)

    def shuffle(self):
        for card in self.cards:
            if card.owner == DISCARD_PILE and card.discarded:
                card.shuffle()

    def draw(self, player, num_times=1):
        for times in range(num_times):
            selection = self.__in_deck__()
            random.choice(selection).draw(player)


class Card:
    SUITS = {0: "♠", 1: "♣", 2: "♦", 3: "♥"}
    FACES = {0: "A", 1: "J", 2: "Q", 3: "K"}

    def __init__(self, suit, value):
        self.suit = self.SUITS[suit]
        self.value = value
        self.face = True if self.value > 10 else False
        self.printed = self.suit + str(self.value) if not self.face else self.suit + str(self.FACES[value - 11])
        self.owner = DECK
        self.discarded = False
        self.drawn = False

    def card_form(self):
        return "[" + self.printed + "]"

    def show(self):
        print(self.card_form())

    def draw(self, player):
        self.drawn = True
        self.owner = player

    def discard(self):
        self.owner = DISCARD_PILE
        self.discarded = True

    def shuffle(self):
        self.owner = DECK
        self.drawn = False
        self.discarded = False


if __name__ == "__main__":
    pass
