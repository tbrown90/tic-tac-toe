"""Simple Tic-Tac-Toe game playable from the command line."""

import sys

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


def main():
    board = [""] * 9
    current = "X"
    while True:
        print_board(board)
        move = get_move(board, current)
        board[move] = current
        if check_win(board, current):
            print_board(board)
            print(f"Player {current} wins!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current = "O" if current == "X" else "X"


if __name__ == "__main__":
    main()
