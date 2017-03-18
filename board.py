from piece import Piece
import curses

class FullSquareException(Exception):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

class SizeException(Exception):
    def __init__(self, size):
        self.size = size

class Board(object):
    def __init__(self, *args):
        self.data = [[None for i in range(4)] for j in range(4)]

        if len(args) > 0 and type(args[0]) is Board:
            for i in range(4):
                for j in range(4):
                    if type(args[0].data[i][j]) is Piece:
                        # This makes new copies of the pieces on the original
                        # board; this may be overkill.
                        self.data[i][j] = Piece(*args[0].data[i][j].piece)

    def placePiece(self, whichPiece, X, Y):
        if X > 3 or X < 0 or Y > 3 or Y < 0:
            raise IndexError
        if self.data[X][Y] is not None:
            raise FullSquareException(X, Y)

        self.data[X][Y] = whichPiece

        return self

    def removePiece(self, X, Y):
        if X > 3 or X < 0 or Y > 3 or Y < 0:
            raise IndexError

        P = self.data[X][Y]
        self.data[X][Y] = None

        return P

    def hasWon(self):
        rows = [self.checkSet(self.data[i]) for i in range(4)]
        cols = [self.checkSet([self.data[j][i] for j in range(4)]) for i in range(4)]
        diag = self.checkSet([self.data[i][i] for i in range(4)])
        antidiag = self.checkSet([self.data[i][3-i] for i in range(4)])

        return any(rows) or any(cols) or diag or antidiag

    def checkSet(self, group):
        if len(group) != 4:
            raise SizeException(len(group))

        if None in group:
            return False

        for i in range(4):
            s = sum([group[j].type()[i] for j in range(4)])
            if s == 0 or s == 4:
                return True

        return False

    def draw(self, stdscr, highlight=-1):
        for i in range(4):
            for j in range(4):
                Piece.drawBlank(stdscr, i * 5 + 2, (j + 1) * 5 - 1,
                            [highlight // 4, highlight % 4] == [i, j])
                if self.data[i][j] is not None:
                    self.data[i][j].draw(stdscr, (i + 1) * 5 + 1, (j + 1) * 5 - 1,
                            [highlight // 4, highlight % 4] == [i, j])

    def Pieces(self):
        out = []
        for i in range(4):
            for j in range(4):
                if self.data[i][j] is not None:
                    out.append((self.data[i][j], i, j))
        return out

    def emptyTiles(self):
        out = []
        for i in range(4):
            for j in range(4):
                if self.data[i][j] is None:
                    out.append((i, j))
        return out

if __name__ == "__main__":
    B = Board()
    B.placePiece(Piece(0,0,0,0), 0, 0)
    B.placePiece(Piece(0,1,0,0), 0, 1)
    B.placePiece(Piece(0,0,1,0), 0, 2)
    B.placePiece(Piece(0,0,0,1), 0, 3)
    print(B.hasWon())
