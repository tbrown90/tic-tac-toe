import unittest

from src import tic_tac_toe


class TestTicTacToe(unittest.TestCase):
    def test_check_win_rows(self):
        board = ["X", "X", "X", "", "", "", "", "", ""]
        self.assertTrue(tic_tac_toe.check_win(board, "X"))

    def test_check_win_columns(self):
        board = ["O", "", "", "O", "", "", "O", "", ""]
        self.assertTrue(tic_tac_toe.check_win(board, "O"))

    def test_check_win_diagonals(self):
        board = ["X", "", "", "", "X", "", "", "", "X"]
        self.assertTrue(tic_tac_toe.check_win(board, "X"))

    def test_no_win(self):
        board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]
        self.assertFalse(tic_tac_toe.check_win(board, "X"))
        self.assertFalse(tic_tac_toe.check_win(board, "O"))

    def test_draw(self):
        board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]
        self.assertTrue(tic_tac_toe.is_draw(board))
        board[0] = ""
        self.assertFalse(tic_tac_toe.is_draw(board))

    def test_bot_beginner_move(self):
        board = ["X", "O", "", "", "", "", "", "", ""]
        move = tic_tac_toe.get_bot_move(board, "X", "beginner", "O")
        self.assertIn(move, range(9))
        self.assertEqual(board[move], "")

    def test_bot_intermediate_block(self):
        # bot O should block X win
        board = ["X", "X", "", "", "", "", "", "", ""]
        move = tic_tac_toe.get_bot_move(board, "O", "intermediate", "X")
        self.assertEqual(move, 2)

    def test_bot_expert_optimal(self):
        # With expert level, bot should never lose from starting position
        board = [""] * 9
        move = tic_tac_toe.get_bot_move(board, "X", "expert", "O")
        self.assertIn(move, range(9))

    def test_celebration_runs(self):
        # basic smoke test to ensure celebration doesn't crash
        try:
            tic_tac_toe.celebration("Player X")
        except Exception as e:
            self.fail(f"celebration raised an exception: {e}")

    def test_game_state(self):
        state = tic_tac_toe.GameState()
        self.assertTrue(state.make_move(0))
        self.assertFalse(state.make_move(0), "can't move on occupied cell")
        state.current = "X"
        self.assertEqual(state.winner(), None)
        state.board = ["X", "X", "X"] + [""] * 6
        self.assertEqual(state.winner(), "X")


if __name__ == "__main__":
    unittest.main()
