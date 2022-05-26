from django.test import TestCase
# Create your tests here.


from terminal_version import game

class TableViewTestCase(TestCase):

    def test_player_can_see_stack_size(self):
        self.fail("not implemented")

    def test_player_can_see_pot_size(self):
        self.fail("not implemented")

    def test_player_can_see_other_players(self):
        self.fail("not implemented")

    def test_player_can_see_other_players_stack_size(self):
        self.fail("not implemented")

    def test_player_can_see_current_turn(self):
        self.fail("not implemented")

    def test_player_can_see_past_actions(self):
        self.fail("not implemented")

    def test_player_can_cycle_turn(self):
        self.fail("not implemented")

    def test_player_can_bet_on_turn(self):
        self.fail("not implemented")

    def test_player_can_burn_on_turn(self):
        self.fail("not implemented")

    def test_player_can_swap_3_or_less_cards_on_swap(self):
        self.fail("not implemented")

    def test_player_cant_swap_or_bet_oobounds(self):
        self.fail("not implemented")

    def test_player_can_leave_table(self):
        self.fail("not implemented")


class DirectoryViewTestCase(TestCase):
    def test_player_can_add_table(self):
        self.fail("not implemented")

    def test_player_can_remove_owned_table(self):
        self.fail("not implemented")

    def test_player_can_logout_to_login_view(self):
        self.fail("not implemented")

    def test_player_can_join_a_room(self):
        self.fail("not implemented")

    def test_player_cannot_do_unauthorized_actions(self):
        self.fail("not implemented")

    def test_admins_can_do_all_actions(self):
        self.fail("not implemented")

    def test_player_can_be_assigned_roles(self):
        self.fail("not implemented")

    def test_player_assigned_player_role_default(self):
        self.fail("not implemented")


class LoginViewTestCase(TestCase):
    def test_user_cannot_login_with_invalid_creds(self):
        self.fail("not implemented")

    def test_user_can_login_with_valid_creds(self):
        self.fail("not implemented")

    def test_user_can_register_login_to_sign_up(self):
        self.fail("not implemented")

    def test_player_is_loaded_on_login(self):
        self.fail("not implemented")

    def test_player_table_persistence_kept(self):
        self.fail("not implemented")

    def test_player_loses_table_data_on_leave(self):
        self.fail("not implemented")

    def test_player_loses_table_data_on_logout(self):
        self.fail("not implemented")

    def test_player_roles_saved_in_login(self):
        self.fail("not implemented")

    def test_player_cant_log_in_other_pages(self):
        self.fail("not implemented")


class SignUpViewTestCase(TestCase):
    def test_player_cant_sign_up_as_existing_player(self):
        self.fail("not implemented")

    def test_player_cant_sign_up_on_other_pages(self):
        self.fail("not implemented")

    def test_player_record_made_when_signed_up(self):
        self.fail("not implemented")

    def test_player_can_login_after_signing_up(self):
        self.fail("not implemented")

    def test_player_can_get_to_login_after_signup(self):
        self.fail("not implemented")


class GameTestCase(TestCase):
    # Card Tests:
    def test_card_created_has_correct_value_suit_and_hand_math(self):
        self.fail("not implemented")

    def test_card_can_move_zones(self):
        self.fail("not implemented")

    def test_card_can_move_owners(self):
        self.fail("not implemented")

    # Deck Tests:
    def test_deck_can_load_state(self):
        self.fail("not implemented")

    def test_deck_can_deal(self):
        self.fail("not implemented")

    def test_deck_can_shuffle_properly(self):
        self.fail("not implemented")

    def test_deck_can_discard(self):
        self.fail("not implemented")

    # Player Tests:
    def test_cant_do_action_oobound(self):
        self.fail("not implemented")

    def test_player_can_fold(self):
        self.fail("not implemented")

    def test_player_collects_pot_on_win(self):
        self.fail("not implemented")

    def test_player_can_leave(self):
        self.fail("not implemented")

    def test_player_can_join(self):
        self.fail("not implemented")

    def test_player_can_draw(self):
        self.fail("not implemented")

    def test_player_can_take_turn(self):
        self.fail("not implemented")

    def test_player_can_pass(self):
        self.fail("not implemented")

    def test_player_can_swap(self):
        self.fail("not implemented")

    def test_player_can_bet(self):
        self.fail("not implemented")

    def test_player_can_burn(self):
        self.fail("not implemented")

    # Hand Tests:
    def test_has_hand_size_of_deal(self):
        test_table = game.Table([])
        self.assertEqual(len(test_table.you.hand.cards), 0)
        test_table.deck.deal(test_table.you, 5)
        self.assertEqual(len(test_table.you.hand.cards), 5)

    def test_player_has_correct_hand_reading(self):
        self.fail("not implemented")
