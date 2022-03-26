from django.test import TestCase
# Create your tests here.


from terminal_version import game


class GameTestCase(TestCase):
    # Card Tests:

    # Deck Tests:

    # Player Tests:

    # Hand Tests:
    def test_has_hand_size_of_deal(self):
        test_table = game.Table([])
        self.assertEqual(len(test_table.you.hand.cards), 0)
        test_table.deck.deal(test_table.you, 5)
        self.assertEqual(len(test_table.you.hand.cards), 5)
