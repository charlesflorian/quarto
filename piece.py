import curses
import random

class InvalidPieceException(Exception):
    def __init__(self, *args):
        self.args = args

class OffScreenException(Exception):
    def __init__(self, row, col):
        self.row = row
        self.col = col

class NotInBagException(Exception):
    def __init__(self, piece):
        self.piece = piece

class Piece(object):
    def __init__(self, *args):
        if len(args) != 4:
            raise InvalidPieceException(args)

        for i in args:
            if i not in [0, 1]:
                raise InvalidPieceException(args)

        self.piece = args

    def __eq__(self, other):
        if other == None:
            return False
        return self.type() == other.type()

    def __str__(self):
        out = ""
        out += "Tall, " if self.piece[0] else "Short, "
        out += "Dark Brown, " if self.piece[1] else "Light Brown, "
        out += "Round, " if self.piece[2] else "Square, "
        out += "and Concave" if self.piece[3] else "and Flat"
        return out

    def type(self):
        return self.piece

    # TODO: This is sort of crappy. The X, Y on this do not match
    #       the X, Y on draw()
    @staticmethod
    def drawBlank(stdscr, X, Y, highlight=False):
        color = 3 if highlight else 1
        for i in range(5):
            for j in range(3):
                stdscr.move(X + i, Y + j)
                stdscr.addch(0x20, curses.color_pair(color))

    @staticmethod
    def BottomRow():
        return [curses.ACS_LLCORNER, curses.ACS_HLINE, curses.ACS_LRCORNER]

    @staticmethod
    def TopRow(which):
        return [[curses.ACS_ULCORNER, curses.ACS_HLINE, curses.ACS_URCORNER],
                [curses.ACS_ULCORNER, curses.ACS_TTEE, curses.ACS_URCORNER]][which]

    @staticmethod
    def MiddleRow(which):
        return [[curses.ACS_VLINE, 0x20, curses.ACS_VLINE],
                [curses.ACS_VLINE, curses.ACS_DIAMOND, curses.ACS_VLINE]][which]

    def draw(self, stdscr, X, Y, highlight=False):
        """
        X and Y will be of the bottom left corner of the piece
        """
        whichColor = self.piece[1] + 1 # Artifact of how curses labels colors

        if highlight:
            whichColor += 2 # Switch to the white background

        #if X < 4:
        #    raise OffScreenException(X, Y)

        row = X

        bottom = Piece.BottomRow()
        middle = Piece.MiddleRow(self.piece[2])
        top = Piece.TopRow(self.piece[3])

        for i in range(3):
            stdscr.move(row, Y + i)
            stdscr.addch(bottom[i], curses.color_pair(whichColor))

        row -= 1
        for i in range(1 + 2 * self.piece[0]):
            for j in range(3):
                stdscr.move(row, Y + j)
                stdscr.addch(middle[j], curses.color_pair(whichColor))
            row -= 1

        for i in range(3):
            stdscr.move(row, Y + i)
            stdscr.addch(top[i], curses.color_pair(whichColor))
        row -= 1

        for i in range(2 * (1 - self.piece[0])):
            for j in range(3):
                stdscr.move(row, Y + j)
                stdscr.addch(0x20, curses.color_pair(whichColor))
            row -= 1



if __name__ == "__main__":
    P = Piece(1, 1, 1, 1)
    print(P)
