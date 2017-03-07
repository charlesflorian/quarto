from piece import Piece
from bag import Bag
from board import Board
from game import Game

class AI(object):
    def __init__(self, board, bag, piece, depth=16):
        assert(type(board) is Board)
        assert(type(bag) is Bag)
        assert(type(piece) is Piece)
        self.board = Board(board)
        self.bag = Bag(bag)
        self.piece = Piece(*piece.piece)

    def nextMove(self):
        for x, y in self.board.emptyTiles():
            if Board(self.board).placePiece(self.piece, x, y).hasWon():
                return (x, y)

    def nextPiece(self):
        pass

if __name__ == "__main__":
    ai = AI(Board(), Bag(), Piece(1,1,1,1))
