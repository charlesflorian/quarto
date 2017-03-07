import curses
import random
from piece import Piece

class Bag(object):
    def __init__(self, *args):
        self.bag = []
        if len(args) > 0 and type(args[0]) is Bag:
            self.bag = args[0].bag[:]
        else:
            for i in range(16):
                color = i % 2
                height = (i >> 1) % 2
                shape = (i >> 2) % 2
                concave = (i >> 3) % 2
                self.bag.append(Piece(color, height, shape, concave))
            random.shuffle(self.bag)

    def __str__(self):
        out = "Remaining Pieces:\n"
        for piece in self.bag:
            out += str(piece) + "\n"
        return out

    def __len__(self):
        return len(self.bag)

    def __iter__(self):
        return self.bag

    def isIn(self, piece):
        return piece in self.bag

    def remove(self, idx):
        if idx < 0 or idx >= len(self.bag):
            raise IndexError
        return self.bag.pop(idx)

    def draw(self, stdscr, highlight=-1):
        for i in range(16):
            X = i % 4
            Y = i // 4
            if i < len(self.bag):
                self.bag[i].draw(stdscr, (Y + 1) * 5 + 1, (X + 10) * 5,
                    [highlight // 4, highlight % 4] == [Y, X])
            else:
                Piece.drawBlank(stdscr, (Y + 1) * 5 - 3, (X + 10) * 5, False)
