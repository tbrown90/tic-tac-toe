"""Simple Tic-Tac-Toe game playable from the command line."""

import sys
import random
import time

BOARD_TEMPLATE = [str(i) for i in range(1, 10)]


def print_board(board):
    cells = [board[i] if board[i] in ["X", "O"] else str(i + 1) for i in range(9)]
    print(f"{cells[0]} | {cells[1]} | {cells[2]}")
    print("---------")
    print(f"{cells[3]} | {cells[4]} | {cells[5]}")
    print("---------")
    print(f"{cells[6]} | {cells[7]} | {cells[8]}")


def check_win(board, player):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def is_draw(board):
    return all(space in ["X", "O"] for space in board)


def get_move(board, player):
    """Prompt a human player for a move."""
    while True:
        try:
            choice = int(input(f"Player {player}, enter move (1-9): ")) - 1
            if choice < 0 or choice >= 9:
                raise ValueError
            if board[choice] in ["X", "O"]:
                print("That space is already taken.")
                continue
            return choice
        except ValueError:
            print("Invalid input; please enter a number between 1 and 9.")


def select_mode():
    print("Choose game mode:")
    print("1. Human vs Human")
    print("2. Human vs Bot")
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            return choice
        print("Invalid selection.")


def select_skill():
    print("Select bot skill level:")
    print("1. Beginner")
    print("2. Intermediate")
    print("3. Expert")
    while True:
        choice = input("Enter 1, 2 or 3: ").strip()
        if choice == "1":
            return "beginner"
        if choice == "2":
            return "intermediate"
        if choice == "3":
            return "expert"
        print("Invalid selection.")


def get_bot_move(board, player, level, human_player):
    """Choose a bot move based on the skill level."""
    avail = [i for i in range(9) if board[i] == ""]
    if level == "beginner":
        return random.choice(avail)
    if level == "intermediate":
        # win if possible
        for i in avail:
            board[i] = player
            if check_win(board, player):
                board[i] = ""
                return i
            board[i] = ""
        # block opponent
        opp = "O" if player == "X" else "X"
        for i in avail:
            board[i] = opp
            if check_win(board, opp):
                board[i] = ""
                return i
            board[i] = ""
        return random.choice(avail)
    if level == "expert":
        # minimax
        def minimax(bd, current, bot, human):
            if check_win(bd, bot):
                return 1
            if check_win(bd, human):
                return -1
            if is_draw(bd):
                return 0
            moves = [i for i in range(9) if bd[i] == ""]
            if current == bot:
                best = -float("inf")
                for m in moves:
                    bd[m] = current
                    score = minimax(bd, human, bot, human)
                    bd[m] = ""
                    best = max(best, score)
                return best
            else:
                best = float("inf")
                for m in moves:
                    bd[m] = current
                    score = minimax(bd, bot, bot, human)
                    bd[m] = ""
                    best = min(best, score)
                return best
        best_val = -float("inf")
        best_move = avail[0]
        for m in avail:
            board[m] = player
            val = minimax(board, human_player, player, human_player)
            board[m] = ""
            if val > best_val:
                best_val = val
                best_move = m
        return best_move
    # fallback
    return random.choice(avail)


def celebration(winner):
    firework = [
        "        .",
        "       ...",
        "      .....",
        "     .......",
        "    .........",
        "      .'.",
        "   .''.'.''",
        "  '.''.'.''.'",
        "   '._.' '._.'",
    ]
    print(f"{winner} wins!")
    for _ in range(3):
        for frame in firework:
            print(frame)
            time.sleep(0.1)
        # clear lines
        for _ in firework:
            sys.stdout.write("\033[F\033[K")
    print(f"{winner} wins!\n")


def main():
    mode = select_mode()
    board = [""] * 9
    human_player = "X"
    bot_player = "O"
    bot_level = None
    if mode == "2":
        bot_level = select_skill()
        first = input("Do you want to go first? (y/n): ").lower().startswith("y")
        if not first:
            human_player, bot_player = bot_player, human_player
    current = "X"
    while True:
        print_board(board)
        if mode == "2" and current == bot_player:
            move = get_bot_move(board, current, bot_level, human_player)
            print(f"Bot ({bot_level}) chooses {move + 1}")
        else:
            move = get_move(board, current)
        board[move] = current
        if check_win(board, current):
            print_board(board)
            winner = "Bot" if mode == "2" and current == bot_player else f"Player {current}"
            celebration(winner)
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current = "O" if current == "X" else "X"


if __name__ == "__main__":
    main()
