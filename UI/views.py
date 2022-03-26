from django.shortcuts import render
from game_obj.models import TableModel
from game_obj.TableController import TableController


def update_table(table, model):
    state_tuple = table.save_state()
    model.state = state_tuple[0]
    model.user_name = state_tuple[1]
    model.user_hand = state_tuple[2]
    model.user_stack = state_tuple[3]
    model.player_names = state_tuple[4]
    model.player_hands = state_tuple[5]
    model.player_stacks = state_tuple[6]
    model.hand_name = table.you.hand.name
    model.phase = table.get_state()
    model.user_stack_length = len(state_tuple[3])
    model.save()


def update_local_table(table, model):
    table.load_state(model.state, model.user_name, model.user_hand, model.user_stack, model.player_names,
                     model.player_hands, model.player_stacks)


def __burn__button__handle(table, model):
    table.burn_button()
    update_table(table, model)



def __bet__button__handle(table, model):
    table.bet_button()
    update_table(table, model)


def __pass__button__handle(table, model):
    table.pass_button()
    update_table(table, model)


def __fold__button__handle(table, model):
    table.fold_button()
    update_table(table, model)


def geeks_view(request):
    # create a dictionary to pass
    # data to the template
    our_table = TableController()
    if len(TableModel.objects.all()) < 1:
        our_model = TableModel.objects.create(state=our_table.state, user_name=our_table.you.name,
                                              user_hand=our_table.you.hand.show_unicode(),
                                              user_stack=our_table.you.hand.show_stack_unicode(),
                                              player_names=our_table.get_names(),
                                              player_hands=our_table.get_player_hands(),
                                              player_stacks=our_table.get_player_stacks(),
                                              user_stack_length=len(our_table.you.hand.stack),
                                              phase=our_table.get_state(),
                                              table_log="", hand_name=our_table.you.hand.name)
        our_model.save()
    else:
        our_model = TableModel.objects.get()
        update_local_table(our_table, our_model)

    context = {
        "state": our_model.state,
        "user_name": our_model.user_name,
        "user_hand": our_model.user_hand,
        "user_stack": our_model.user_stack,
        "player_names": our_model.player_names,
        "player_stacks": our_model.player_stacks,
        "burn_button": __burn__button__handle(our_table, our_model),
        "bet_button": __bet__button__handle(our_table, our_model),
        "fold_button": __fold__button__handle(our_table, our_model),
        "pass_button": __pass__button__handle(our_table, our_model),
        "phase": our_model.phase,
        "user_stack_length": our_model.user_stack_length,
        "hand_name": our_model.hand_name,
    }
    # return response with template and context
    return render(request, "geeks.html", context)
