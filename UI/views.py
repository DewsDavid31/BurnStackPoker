from django.shortcuts import render
from game.game import Deck, Player


def geeks_view(request):
    # create a dictionary to pass
    # data to the template

    test_deck = Deck()
    test_player = Player("test_player")
    Deck.deal(test_deck, test_player, 5)
    Deck.deal_stack(test_deck, test_player,5)
    test_player.hand.calculate_rank()

    context = {
        "hand": test_player.hand.show_unicode(),
        "stack": len(test_player.hand.stack),
        "hand_name": test_player.hand.name,
        "actual": test_player.hand.show_string(),
    }
    # return response with template and context
    return render(request, "geeks.html", context)
