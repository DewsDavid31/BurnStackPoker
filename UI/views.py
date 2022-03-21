from django.shortcuts import render
from game_obj.models import PlayerModel
from game_obj.game import Deck, Player, Table


def __next_phase__(test_table):
    test_table.next_phase()
    p = PlayerModel.objects.get(name='you')
    p.phase = test_table.state
    p.hand = test_table.you.hand.show_unicode()
    test_table.you.hand.calculate_rank()
    p.hand_name = test_table.you.hand.name
    p.stack = len(test_table.you.hand.stack)
    p.save()


def __bet__(test_table):
    test_table.you.bet()
    p = PlayerModel.objects.get(name='you')
    p.stack = len(test_table.you.hand.stack)
    p.save()


def __burn__(test_table):
    test_table.you.burn(1)
    test_table.you.hand.calculate_rank()
    p = PlayerModel.objects.get(name='you')
    p.stack = len(test_table.you.hand.stack)
    p.hand = test_table.you.hand.show_unicode()
    p.hand_name = test_table.you.hand.name
    p.save()


def geeks_view(request):
    # create a dictionary to pass
    # data to the template

    if len(PlayerModel.objects.filter(name='you')) < 1:
        test_table = Table([])
        test_table.next_phase()
        p = PlayerModel.objects.create(name='you', hand_name=test_table.you.hand.name,
                                       hand=test_table.you.hand.show_unicode(), stack=len(test_table.you.hand.stack),
                                       phase=test_table.state)
        p.save()
    else:
        p = PlayerModel.objects.get(name='you')
        test_table = Table([])
        test_table.load(p.name, p.hand, p.stack)
    context = {
        "phase": PlayerModel.objects.filter(name='you')[0].phase,
        "hand": PlayerModel.objects.filter(name='you')[0].hand,
        "stack": PlayerModel.objects.filter(name='you')[0].stack,
        "hand_name": PlayerModel.objects.filter(name='you')[0].hand_name,
        "bet": __bet__(test_table),
        "burn": __burn__(test_table),
        "pass": __next_phase__(test_table),
    }
    # return response with template and context
    return render(request, "geeks.html", context)
