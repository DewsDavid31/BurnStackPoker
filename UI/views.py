from django.shortcuts import render
from game.game import Deck, Player, Table


def geeks_view(request):
    # create a dictionary to pass
    # data to the template

    test_table = Table([])
    test_table.next_phase()

    context = {
        "hand": test_table.you.hand.show_unicode(),
        "stack": len(test_table.you.hand.stack),
        "hand_name": test_table.you.hand.name,
        "actual": test_table.you.hand.show_string(),
        "bet": test_table.you.bet(),
        "burn": test_table.you.burn(1),
        "pass": test_table.next_phase(),
    }
    # return response with template and context
    return render(request, "geeks.html", context)
