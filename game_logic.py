import time


class Game:

    """the minimax algorithm"""

    def __init__(self, gui):
        self.player_turn = None
        self.initialize_game()
        self.gui = gui

    def initialize_game(self):
        self.game_state = [["." for j in range(3)] for i in range(3)]
        self.player_turn = "X"

    def draw_board(self):
        for i, row in enumerate(self.game_state):
            temp_row = []
            for j, cell in enumerate(row):
                if j != 2:
                    cell = f"{cell} |"
                temp_row.append(cell)
                print(cell, end="")
            print()
            if i != 2:
                print("-" * len("".join(temp_row)), end="")
                print()

    def game_ended(self):

        # horizontal check
        for i in range(3):
            row = set([c for c in self.game_state[i]])
            if len(row) == 1 and list(row)[0] != ".":
                return list(row)[0]

        # vertical check
        for j in range(3):
            column = [self.game_state[i][j] for i in range(3)]
            if len(set(column)) == 1 and column[0] != ".":
                return column[0]

        # main diagonal check
        j = 0
        main_diagonal = []
        for i in range(3):
            main_diagonal.append(self.game_state[i][j])
            j += 1
        if len(set(main_diagonal)) == 1 and main_diagonal[0] != ".":
            return main_diagonal[0]

        # second diagonal check
        j = 2
        second_diagonal = []
        for i in range(3):
            second_diagonal.append(self.game_state[i][j])
            j -= 1
        if len(set(second_diagonal)) == 1 and second_diagonal[0] != ".":
            return second_diagonal[0]

        # board is full
        for row in self.game_state:
            if "." in row:
                return None

        # game tie and board is full
        return "."

    def is_valid(self, r, c):
        return (
            (r <= 2 and r >= 0)
            and (c <= 2 and c >= 0)
            and (self.game_state[r][c] == ".")
        )

    def min(self):

        min_value = 2  # worse than worst case scenario

        result = self.game_ended()

        if result == "X":
            return (-1, 0, 0)
        elif result == "O":
            return (1, 0, 0)
        elif result == ".":
            return (0, 0, 0)

        min_x, min_y = None, None

        for i in range(3):
            for j in range(3):
                if self.game_state[i][j] == ".":
                    self.game_state[i][j] = "X"
                    m, mx, my = self.max()
                    if m < min_value:
                        min_value, min_x, min_y = m, i, j
                    self.game_state[i][j] = "."

        return min_value, min_x, min_y

    def max(self):
        max_value = -2  # worse than worst case scenario

        result = self.game_ended()
        if result == "X":
            return (-1, 0, 0)
        elif result == "O":
            return (1, 0, 0)
        elif result == ".":
            return (0, 0, 0)

        max_x, max_y = None, None

        for i in range(3):
            for j in range(3):
                if self.game_state[i][j] == ".":
                    self.game_state[i][j] = "O"
                    m, mx, my = self.min()
                    if m > max_value:
                        max_value, max_x, max_y = m, i, j
                    self.game_state[i][j] = "."

        return max_value, max_x, max_y

    def check_game_ended(self):
        result = self.game_ended()
        if result:
            if result == "X":
                # print('X won the game')
                self.gui.update_startbutton("X won the game")
                self.gui.update_winstats('X')
            elif result == "O":
                # print('O won the game')
                self.gui.update_startbutton("O won the game")
                self.gui.update_winstats('O')
            elif result == ".":
                # print('It is a TIE')
                self.gui.update_startbutton("It is a TIE")
                self.gui.update_winstats('.')
            self.gui.game_ended = True
            return True
        return False

    def play(self):
        self.gui.game_ended = False
        while True:
            if self.player_turn == "X":
                if self.check_game_ended():
                    return

                self.gui.update_startbutton(f'{self.player_turn}"s turn')
                while self.gui.row == None and self.gui.col == None:
                    time.sleep(0.001)
                    continue

                self.game_state[self.gui.row][self.gui.col] = "X"
                self.gui.row, self.gui.col = None, None
                self.player_turn = "O"
                self.gui.update_startbutton(f'{self.player_turn}"s turn')

            if self.player_turn == "O":
                if self.check_game_ended():
                    return
                max_value, max_x, max_y = self.max()
                self.game_state[max_x][max_y] = "O"
                self.gui.board_dict[max_x][max_y].image_src_base64 = self.gui.player_o
                time.sleep(1)  # to simulate thinking process of the AI...
                self.gui.board_dict[max_x][max_y].update()
                self.player_turn = "X"
                self.gui.update_startbutton(f'{self.player_turn}"s turn')
