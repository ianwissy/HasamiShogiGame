# Ian Wyse
# 11/11/2021
# Contains a class allowing the user to play the Hasami Shogi Game.

def to_num(char):
    return ord(char) - ord("`")


class HasamiShogiGame:
    """Class for Hasami Shogi Game. Players make their moves with the make_move method by inputting the location
    of the piece they want to move and the location they want to move it to. Black moves first."""

    def __init__(self):
        """Initializes a new Hasami Shogi game. Sets the game state to unfinished, the board to its starting state,
        the captured values to 0, and gives black the first move."""
        self._game_state = "UNFINISHED"
        self._active_player = "BLACK"
        self._board = [[" ", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                       ["a", "R", "R", "R", "R", "R", "R", "R", "R", "R"],
                       ["b", '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ["c", '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ["d", '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ["e", '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ["f", '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ["g", '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ["h", '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ["i", 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']]
        self._red_captured = 0
        self._black_captured = 0

    def get_game_state(self):
        """Returns the current state of the game."""
        return self._game_state

    def get_active_player(self):
        """Returns the active player."""
        return self._active_player

    def get_num_captured_pieces(self, color):
        """Returns the number of pieces captured by the player entered. 'RED' for the red player, 'BLACK' for the
        black player."""
        if color == 'RED':
            return self._red_captured
        elif color == 'BLACK':
            return self._black_captured

    def get_square_occupant(self, square):
        """Returns the occupant of a given square. If the square contains a red piece, returns 'RED', if the
        square contains a black piece, returns 'BLACK'. If the square is empty, returns 'NONE'."""
        if self._board[to_num(square[0])][int(square[1])] == "B":
            return "BLACK"
        elif self._board[to_num(square[0])][int(square[1])] == "R":
            return "RED"
        else:
            return "NONE"

    def inc_capture_count(self, active_color):
        """Increments the capture counter of the active player."""
        if active_color == "R":
            self._red_captured += 1
        else:
            self._black_captured += 1

    def valid_move(self, piece, target):
        """Checks whether the move entered is valid. If it is not, returns 0, otherwise returns None."""
        if self._game_state == "FINISHED":
            return 0
        if self.get_square_occupant(piece) != self.get_active_player():
            return 0
        if piece[0] != target[0] and piece[1] != target[1]:
            return 0
        if piece[0] == target[0]:
            if piece[1] == target[1]:
                return 0
            elif int(piece[1]) < int(target[1]):
                for column in range(int(piece[1]) + 1, int(target[1]) + 1):
                    if self._board[to_num(piece[0])][column] != '.':
                        return 0
            else:
                for column in range(int(target[1]), int(piece[1])):
                    if self._board[to_num(piece[0])][column] != '.':
                        return 0
        elif to_num(piece[0]) < to_num(piece[0]):
            for row in range(to_num(piece[0]) + 1, to_num(target[0]) + 1):
                if self._board[row][int(piece[1])] != '.':
                    return 0
        else:
            for row in range(to_num(target[0]), to_num(piece[0])):
                if self._board[row][int(piece[1])] != '.':
                    return 0
        return

    def capture(self, target):
        """Captures all pieces caused by the move to the target location."""
        row = to_num(target[0])
        col = int(target[1])
        for direction in range(4):
            self.direction_capture(row, col, direction)
        self.corner_capture()

    def direction_capture(self, row, column, direction):
        """Recursive function to capture non-corner pieces. Checks to see if the square in a given direction from a
        starting location contains a piece.  If it does, and that piece is of the opposing color, performs a check on
        the next square in the same direction. Continues until it either reaches an unclaimed square, or
        a square of the original color. If it finds a square of the original color, captures all pieces it has iterated
         over."""
        row += ((direction + 1) % 2)*(direction - 1)
        column += (direction % 2)*(2 - direction)
        try:
            if self._board[row][column] not in {"R", "B", "."}:
                return
        except IndexError:
            return
        if self._board[row][column] == ".":
            return
        if self._board[row][column] in {"R", "B"}:
            if self._board[row][column] == self._active_player[0]:
                return "CAPTURE"
            else:
                capture = self.direction_capture(row, column, direction)
                if capture == "CAPTURE":
                    self._board[row][column] = '.'
                    self.inc_capture_count(self._active_player[0])
                    return "CAPTURE"
                return

    def corner_capture(self):
        """Captures corner pieces. The method checks all corner locations for captures. If any occur, removes the
        captured piece and iterates the active players capture counter."""
        color_dict = {"R": "B", "B": "R"}
        active_color = self._active_player[0]
        inactive_color = color_dict[active_color]
        if self._board[1][1] == inactive_color and (self._board[1][2] and self._board[2][1]) == active_color:
            self._board[1][1] = '.'
            self.inc_capture_count(active_color)
        elif self._board[1][9] == inactive_color and (self._board[1][8] and self._board[2][9]) == active_color:
            self._board[1][9] = '.'
            self.inc_capture_count(active_color)
        elif self._board[9][1] == inactive_color and (self._board[8][1] and self._board[9][2]) == active_color:
            self._board[9][1] = '.'
            self.inc_capture_count(active_color)
        elif self._board[9][9] == inactive_color and (self._board[9][8] and self._board[8][9]) == active_color:
            self._board[9][9] = '.'
            self.inc_capture_count(active_color)
        return

    def print_board(self):
        """Prints out the board state."""
        for row in range(len(self._board)):
            string = ""
            for column in range(len(self._board)):
                string += self._board[row][column]
                string += " "
            print(string)
        return

    def make_move(self, piece, target):
        """Moves piece from piece location to target location if that move is legal. If that move causes captures,
        captures those pieces and iterates the capture count. Ends the game if 8 pieces are captured by the player,
        otherwise changes the active player to the the opponent."""
        if self.valid_move(piece, target) == 0:
            return False
        self._board[to_num(target[0])][int(target[1])] = self._board[to_num(piece[0])][int(piece[1])]
        self._board[to_num(piece[0])][int(piece[1])] = "."
        self.capture(target)
        # self.print_board()
        if self._active_player == "BLACK":
            if self._black_captured == 8:
                # print("Black Wins!")
                self._game_state = "BLACK_WON"
                return True
            self._active_player = "RED"
            return True
        else:
            if self._red_captured == 8:
                # print("Red Wins!")
                self._game_state = "RED_WON"
                return True
            self._active_player = "BLACK"
            return True
