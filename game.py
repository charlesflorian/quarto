import curses

from piece import Piece
from bag import Bag
from board import Board
from board import FullSquareException

MAX_SCREEN_HEIGHT = 24

class Game(object):
    def __init__(self):
        self.board = Board()
        self.bag = Bag()

        self.nextPiece = None

        self.onBoard = False

        self.highlight = 0

        self.isPlayerOne = True

    def drawBox(self, stdscr, X, Y, width, height):
        for i in range(X + 1, X + 1 + width):
            stdscr.addch(Y, i, curses.ACS_HLINE)
            stdscr.addch(Y + height, i, curses.ACS_HLINE)
        for i in range(Y + 1, Y + 1 + height):
            stdscr.addch(i, X, curses.ACS_VLINE)
            stdscr.addch(i, X + width, curses.ACS_VLINE)
        stdscr.addch(Y,X,curses.ACS_ULCORNER)
        stdscr.addch(Y,X + width,curses.ACS_URCORNER)
        stdscr.addch(Y + height, X,curses.ACS_LLCORNER)
        stdscr.addch(Y + height, X + width, curses.ACS_LRCORNER)

    def drawGame(self, stdscr):
        stdscr.addstr(0, 0, "Game Board")

        self.drawBox(stdscr, 2, 1, 21, 21)

        if self.onBoard:
            self.board.draw(stdscr, self.highlight)
        else:
            self.board.draw(stdscr)

    def drawNextPiece(self, stdscr):
        stdscr.addstr(0, 30, "Next Piece")

        self.drawBox(stdscr, 31, 1, 8, 8)

        if self.nextPiece is not None:
            self.nextPiece.draw(stdscr, 7, 34)
        else:
            Piece.drawBlank(stdscr, 3, 34)

    def drawBag(self, stdscr):
        stdscr.addstr(0, 45, "Remaining tiles")

        self.drawBox(stdscr, 46, 1, 24, 21)

        if not self.onBoard:
            self.bag.draw(stdscr, self.highlight)
        else:
            self.bag.draw(stdscr)

    def draw(self, stdscr):
        self.drawGame(stdscr)
        self.drawBag(stdscr)
        self.drawNextPiece(stdscr)

        if self.isPlayerOne:
            if self.onBoard:
                writeText(stdscr, "Player one: Place Piece")
            else:
                writeText(stdscr, "Player one: Choose Piece")
        else:
            if self.onBoard:
                writeText(stdscr, "Player two: Place Piece")
            else:
                writeText(stdscr, "Player two: Choose Piece")



def initColors():
    curses.start_color()
    curses.curs_set(0)

    curses.init_pair(1, 179, curses.COLOR_BLACK)
    curses.init_pair(2, 94, curses.COLOR_BLACK)

    curses.init_pair(3, 179, curses.COLOR_WHITE)
    curses.init_pair(4, 94, curses.COLOR_WHITE)

def boardMove(G, c):
    if c == curses.KEY_UP:
        G.highlight -= 4
        if G.highlight < 0:
            G.highlight += 4
    elif c == curses.KEY_LEFT:
        G.highlight -= 1
        if G.highlight % 4 == 3:
            G.highlight += 1
    elif c == curses.KEY_RIGHT:
        G.highlight += 1
        if G.highlight % 4 == 0:
            G.highlight -= 1
    elif c == curses.KEY_DOWN:
        G.highlight += 4
        if G.highlight > 15:
            G.highlight -= 4

def bagMove(G, c):
    if c == curses.KEY_UP:
        G.highlight -= 4
        if G.highlight < 0:
            G.highlight += 4
    elif c == curses.KEY_LEFT:
        G.highlight -= 1
        if G.highlight < 0:
            G.highlight = 0
    elif c == curses.KEY_RIGHT:
        G.highlight += 1
        if G.highlight >= len(G.bag):
            G.highlight = len(G.bag) - 1
    elif c == curses.KEY_DOWN:
        G.highlight += 4
        if G.highlight > len(G.bag):
            G.highlight = len(G.bag) - 1

MAX_STR_LEN = 17

def writeToLog(string, append=False):
    if append:
        f = open("out.log", "a")
    else:
        f = open("out.log", "w")
    f.write(string + "\n")
    f.close()

def clearText(stdscr):
    row = 15

    while row < MAX_SCREEN_HEIGHT:
        stdscr.addstr(row, 27, " " * MAX_STR_LEN)
        row += 1

def writeText(stdscr, string):
    clearText(stdscr)
    row = 15
    words = string.split(" ")

    currentLine = words[0]

    for word in words[1:]:
        if len(word) + len(currentLine) + 1 > MAX_STR_LEN:
            stdscr.addstr(row, 27, currentLine)
            row += 1
            currentLine = word
        else:
            currentLine += " " + word

    # Empty the buffer
    stdscr.addstr(row, 27, currentLine)

def main(stdscr):
    initColors()

    G = Game()
    G.draw(stdscr)

    # TODO: Find the right places to draw this, and fix the darn text stuff.

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord(' '):
            if G.onBoard: # Do place the piece!
                try:
                    G.board.placePiece(G.nextPiece, G.highlight // 4, G.highlight % 4)
                except FullSquareException:
                    continue # TODO: whatever I need to make this actually make sense.
                G.nextPiece = None
            else: # Pick the piece!
                G.nextPiece = G.bag.remove(G.highlight)
                G.isPlayerOne = not G.isPlayerOne
            G.onBoard = not G.onBoard
        elif G.onBoard:
            boardMove(G, c)
        else:
            bagMove(G, c)

        G.draw(stdscr)

        if G.board.hasWon():
            if G.isPlayerOne:
                #stdscr.addstr(15, 27, "Player one wins!")
                writeText(stdscr, "Player one wins! This is really great!")
            else:
                #stdscr.addstr(15, 27, "Player two wins!")
                writeText(stdscr, "Player two wins!")

            stdscr.getch()

            stdscr.clear()

            G = Game()
            G.draw(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
