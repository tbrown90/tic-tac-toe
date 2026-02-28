"""Tic-Tac-Toe game with optional GUI front end.

The module defines core logic functions (win checking, draw detection, bot
moves) and also provides a simple Pygame-based graphical interface.  The GUI
uses a cartoonish style with bold lines and bright colors.  When run as a
script the player is prompted for mode/skill via the terminal before the
window appears.
"""

import sys
import random
import time

# GUI dependencies are optional; import when used
try:
    import pygame
except ImportError:
    pygame = None

BOARD_TEMPLATE = [str(i) for i in range(1, 10)]


def print_board(board):
    """Text-based board print used for debugging or early prompts."""
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
    """ASCII firework used in terminal mode. GUI mode has its own effect."""
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


class GameState:
    """Encapsulates board state and current player."""

    def __init__(self, mode="1", bot_level=None, human_first=True):
        self.board = [""] * 9
        self.current = "X"
        self.mode = mode
        self.bot_level = bot_level
        self.human_player = "X" if human_first else "O"
        self.bot_player = "O" if human_first else "X"

    def make_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.current
            return True
        return False

    def advance(self):
        self.current = "O" if self.current == "X" else "X"

    def winner(self):
        if check_win(self.board, self.current):
            return self.current
        return None


def run_gui(state: GameState):
    if pygame is None:
        raise RuntimeError("Pygame is not installed; cannot run GUI mode.")

    pygame.init()
    size = 300
    cell = size // 3
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Tic-Tac-Toe")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    def draw():
        screen.fill((135, 206, 235))  # light blue background
        # grid lines
        for i in range(1, 3):
            pygame.draw.line(screen, (0, 0, 0), (i * cell, 0), (i * cell, size), 4)
            pygame.draw.line(screen, (0, 0, 0), (0, i * cell), (size, i * cell), 4)
        # marks
        for i, mark in enumerate(state.board):
            x = (i % 3) * cell + cell // 2
            y = (i // 3) * cell + cell // 2
            if mark == "X":
                pygame.draw.line(screen, (220, 20, 60), (x - 30, y - 30), (x + 30, y + 30), 8)
                pygame.draw.line(screen, (220, 20, 60), (x + 30, y - 30), (x - 30, y + 30), 8)
            elif mark == "O":
                pygame.draw.circle(screen, (34, 139, 34), (x, y), 30, 8)
        pygame.display.flip()

    running = True
    while running:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                idx = (my // cell) * 3 + (mx // cell)
                if state.mode == "2" and state.current == state.bot_player:
                    continue
                if state.make_move(idx):
                    if state.winner():
                        draw()
                        pygame.time.wait(500)
                        show_message(screen, font, f"Player {state.current} wins!")
                        running = False
                        break
                    if is_draw(state.board):
                        draw()
                        pygame.time.wait(500)
                        show_message(screen, font, "It's a draw!")
                        running = False
                        break
                    state.advance()
                    if state.mode == "2" and state.current == state.bot_player:
                        bm = get_bot_move(state.board, state.current, state.bot_level, state.human_player)
                        state.make_move(bm)
                        if state.winner():
                            draw()
                            pygame.time.wait(500)
                            show_message(screen, font, "Bot wins!")
                            running = False
                            break
                        if is_draw(state.board):
                            draw()
                            pygame.time.wait(500)
                            show_message(screen, font, "It's a draw!")
                            running = False
                            break
                        state.advance()
        clock.tick(30)
    pygame.quit()


def show_message(screen, font, text):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 200))
    screen.blit(overlay, (0, 0))
    msg = font.render(text, True, (0, 0, 0))
    rect = msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(msg, rect)
    pygame.display.flip()
    pygame.time.wait(1500)


def main():
    mode = select_mode()
    bot_level = None
    human_first = True
    if mode == "2":
        bot_level = select_skill()
        first = input("Do you want to go first? (y/n): ").lower().startswith("y")
        human_first = first
    state = GameState(mode=mode, bot_level=bot_level, human_first=human_first)
    # launch GUI
    if pygame:
        run_gui(state)
    else:
        # fallback to CLI
        cli_loop(state)


def cli_loop(state):
    # preserve earlier CLI logic; this is mostly unchanged
    while True:
        print_board(state.board)
        if state.mode == "2" and state.current == state.bot_player:
            move = get_bot_move(state.board, state.current, state.bot_level, state.human_player)
            print(f"Bot ({state.bot_level}) chooses {move + 1}")
        else:
            move = get_move(state.board, state.current)
        state.board[move] = state.current
        if check_win(state.board, state.current):
            print_board(state.board)
            winner = "Bot" if state.mode == "2" and state.current == state.bot_player else f"Player {state.current}"
            celebration(winner)
            break
        if is_draw(state.board):
            print_board(state.board)
            print("It's a draw!")
            break
        state.current = "O" if state.current == "X" else "X"


if __name__ == "__main__":
    main()
