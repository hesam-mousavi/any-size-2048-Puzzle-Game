"""
2048 is an easy and fun puzzle game.
Even if you don't love numbers you will love this game.
It is played on a 3x3 grid or higher using the ↑ → ↓ ← arrows or W, A, S, D keys alternatively.
Every time you press a key - all tiles slide.
Tiles with the same value that bump into one-another are merged.
Although there might be an optimal strategy to play, there is always some level of chance.
If you beat the puzzle and would like to master it, try to finish with a smaller score.
That would mean that you finished with less moves
"""
import random, sys
import colored
from colored import stylize
import math
import keyboard
import os


class Puzzle:
    __colors = {
        4: 245,  # number: color code in colored module,
        8: 237,
        16: 225,
        32: 215,
        64: 205,
        128: 195,
        256: 56,
        512: 183,
        1024: 69,
        2048: 153,
        4096: 143,
        8192: 123,
        16384: 113,
        32768: 103,
        65536: 93,
    }
    # To fill the cells of the puzzle with BLANK
    __BLANK = ""
    # {(1,1)="",(1,2)="",(1,3)="",...,(2,1)="",(2,2)="",...,(size,size)=""} for all cells
    __cellsXY = {}
    __score = 0
    __best_score = 0
    # list of cells for check what cell is empty to add new rand number to it. its create [1,2,3,4, ...,size*size] first because at the beginning of the puzzle, all the cells are empty
    __empty_cells = []
    # size of puzzle, for example 3*3 mode
    __size = 3
    canCreateBoard = True

    def __init__(self, size):
        # puzzle size is dynamic and must be equal or greater than 3
        if int(size) >= 3:
            self.__size = int(size)
            self.setBestScore()
        else:
            sys.exit()

        # fill cells with BLANK and create empty cells list
        self.resetGame()

    def setBestScore(self):
        if os.path.exists("./best-score.txt"):
            with open("best-score.txt", "r") as bs:
                best_score = bs.read()
                if not best_score.isnumeric():
                    best_score = 0
                self.__best_score = int(best_score)

    def __cls(self):
        os.system("cls" if os.name == "nt" else "clear")

    def resetGame(self):
        for x in range(self.__size):
            for y in range(self.__size):
                # if size=3 and __BLANK="", its create {(1,1):"",(1,2):"",(1,3):"",(2,1):"",(2,2):"",(2,3):"",(3,1):"",(3,2):"",(3,3):""}
                self.__cellsXY[(x + 1, y + 1)] = self.__BLANK
        # if new puzzle created or continue puzzle after puzzle over, empty cells must be created
        self.__empty_cells.clear()
        # if size=3, create [1,2,3,4,5,6,7,8,9]
        self.__empty_cells = [x + 1 for x in range(self.__size**2)]
        self.__score = 0
        self.setBestScore()
        self.canCreateBoard = True

    def __addRandNum(self):
        if (
            len(self.__empty_cells) > 0
        ):  # if it is possible to add a new number to the puzzle
            rand_num = random.choice(self.__empty_cells)
            del self.__empty_cells[self.__empty_cells.index(rand_num)]
            self.__cellsXY[
                (self.__getX(rand_num), self.__getY(rand_num))
            ] = random.choice([2, 2, 4])
            self.last_rand = rand_num

    # for example in 3*3 puzzle, cell with number 4 is => (x=2,y=1) or cell with number 8 is => (x=3,y=2), __getX func return x
    def __getX(self, rand):
        return math.ceil(rand / self.__size)

    # this func return y in (x,y) tuple
    def __getY(self, rand):
        if rand % self.__size == 0:
            return self.__size
        else:
            return rand % self.__size

    def canContinue(self):
        # When all the cells are not filled, then the puzzle can still be continued
        if len(self.__empty_cells) > 0:
            return True
        # If all the cells are full, it should be checked whether there are any places to merged or not
        elif len(self.__empty_cells) == 0:
            for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                    if (
                        y + 1 <= self.__size
                        and self.__cellsXY[(x, y)] == self.__cellsXY[(x, y + 1)]
                    ):
                        return True
                    elif (
                        x + 1 <= self.__size
                        and self.__cellsXY[(x, y)] == self.__cellsXY[(x + 1, y)]
                    ):
                        return True
        return False

    # all move and merge funcs update "__cellsXY" and update "__empty_cells" vars in memory then create board with createBoard() func
    def moveUp(self):
        blanks = []
        for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            blanks.clear()
            for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                if self.__cellsXY[(x, y)] == self.__BLANK:
                    blanks.append((x, y))
                    continue
                else:
                    if len(blanks):
                        m, n = blanks[0]
                        self.__cellsXY[(m, n)] = self.__cellsXY[(x, y)]
                        self.__cellsXY[(x, y)] = self.__BLANK
                        del blanks[0]
                        blanks.append((x, y))

                        del self.__empty_cells[
                            self.__empty_cells.index(
                                (m * self.__size) - (self.__size - n)
                            )
                        ]
                        self.__empty_cells.append((x * self.__size) - (self.__size - y))
                        self.canCreateBoard = True

    def mergeUp(self):
        for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                if self.__cellsXY[(x, y)] != self.__BLANK:
                    if x < self.__size and self.__cellsXY[(x + 1, y)] != self.__BLANK:
                        if self.__cellsXY[(x, y)] == self.__cellsXY[(x + 1, y)]:
                            self.__cellsXY[(x, y)] *= 2
                            self.__score += self.__cellsXY[(x, y)]
                            self.__cellsXY[(x + 1, y)] = self.__BLANK
                            self.__empty_cells.append(
                                ((x + 1) * self.__size) - (self.__size - y)
                            )
                            self.canCreateBoard = True

    def moveDown(self):
        blanks = []
        for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            blanks.clear()
            for x in range(self.__size, 0, -1):  # [4, 3, 2, 1]
                if self.__cellsXY[(x, y)] == self.__BLANK:
                    blanks.append((x, y))
                    continue
                else:
                    if len(blanks):
                        m, n = blanks[0]
                        self.__cellsXY[(m, n)] = self.__cellsXY[(x, y)]
                        self.__cellsXY[(x, y)] = self.__BLANK
                        del blanks[0]
                        blanks.append((x, y))

                        del self.__empty_cells[
                            self.__empty_cells.index(
                                (m * self.__size) - (self.__size - n)
                            )
                        ]
                        self.__empty_cells.append((x * self.__size) - (self.__size - y))
                        self.canCreateBoard = True

    def mergeDown(self):
        for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            for x in range(self.__size, 0, -1):  # [4, 3, 2, 1]
                if self.__cellsXY[(x, y)] != self.__BLANK:
                    if x > 1 and self.__cellsXY[(x - 1, y)] != self.__BLANK:
                        if self.__cellsXY[(x, y)] == self.__cellsXY[(x - 1, y)]:
                            self.__cellsXY[(x, y)] *= 2
                            self.__score += self.__cellsXY[(x, y)]
                            self.__cellsXY[(x - 1, y)] = self.__BLANK
                            self.__empty_cells.append(
                                ((x - 1) * self.__size) - (self.__size - y)
                            )
                            self.canCreateBoard = True

    def moveRight(self):
        blanks = []
        for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            blanks.clear()
            for y in range(self.__size, 0, -1):  # [4, 3, 2, 1]
                if self.__cellsXY[(x, y)] == self.__BLANK:
                    blanks.append((x, y))
                    continue
                else:
                    if len(blanks):
                        m, n = blanks[0]
                        self.__cellsXY[(m, n)] = self.__cellsXY[(x, y)]
                        self.__cellsXY[(x, y)] = self.__BLANK
                        del blanks[0]
                        blanks.append((x, y))

                        del self.__empty_cells[
                            self.__empty_cells.index(
                                (m * self.__size) - (self.__size - n)
                            )
                        ]
                        self.__empty_cells.append((x * self.__size) - (self.__size - y))
                        self.canCreateBoard = True

    def mergeRight(self):
        for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            for y in range(self.__size, 0, -1):  # [4, 3, 2, 1]
                if self.__cellsXY[(x, y)] != self.__BLANK:
                    if y > 1 and self.__cellsXY[(x, y - 1)] != self.__BLANK:
                        if self.__cellsXY[(x, y)] == self.__cellsXY[(x, y - 1)]:
                            self.__cellsXY[(x, y)] *= 2
                            self.__score += self.__cellsXY[(x, y)]
                            self.__cellsXY[(x, y - 1)] = self.__BLANK
                            self.__empty_cells.append(
                                (x * self.__size) - (self.__size - (y - 1))
                            )
                            self.canCreateBoard = True

    def moveLeft(self):
        blanks = []
        for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            blanks.clear()
            for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                if self.__cellsXY[(x, y)] == self.__BLANK:
                    blanks.append((x, y))
                    continue
                else:
                    if len(blanks):
                        m, n = blanks[0]
                        self.__cellsXY[(m, n)] = self.__cellsXY[(x, y)]
                        self.__cellsXY[(x, y)] = self.__BLANK
                        del blanks[0]
                        blanks.append((x, y))

                        del self.__empty_cells[
                            self.__empty_cells.index(
                                (m * self.__size) - (self.__size - n)
                            )
                        ]
                        self.__empty_cells.append((x * self.__size) - (self.__size - y))
                        self.canCreateBoard = True

    def mergeLeft(self):
        for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
            for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                if self.__cellsXY[(x, y)] != self.__BLANK:
                    if y < self.__size and self.__cellsXY[(x, y + 1)] != self.__BLANK:
                        if self.__cellsXY[(x, y)] == self.__cellsXY[(x, y + 1)]:
                            self.__cellsXY[(x, y)] *= 2
                            self.__score += self.__cellsXY[(x, y)]
                            self.__cellsXY[(x, y + 1)] = self.__BLANK
                            self.__empty_cells.append(
                                (x * self.__size) - (self.__size - (y + 1))
                            )
                            self.canCreateBoard = True

    def createBoard(self, direction=""):
        # print(chr(27) + "[2J")  # clear terminal
        if self.canCreateBoard == True:
            self.__cls()
            self.__addRandNum()
            top = stylize("+-----", colored.fg("red"))
            liter_line = "{}"

            for x in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                tops = ""
                liter_lines = ""
                for y in range(1, self.__size + 1):  # [1, 2, 3, 4] if size==4
                    tops += top
                    if (
                        self.__getX(self.last_rand) == x
                        and self.__getY(self.last_rand) == y
                    ):
                        liter_lines += stylize("|", colored.fg("red")) + stylize(
                            liter_line.format(self.__cellsXY[(x, y)]).center(5),
                            colored.fg("blue"),
                        )

                    else:
                        liter_lines += stylize("|", colored.fg("red")) + stylize(
                            liter_line.format(self.__cellsXY[(x, y)]).center(5),
                            colored.bg(
                                self.__colors.get(self.__cellsXY[(x, y)], "black")
                            ),
                        )

                print(tops + stylize("+", colored.fg("red")))
                print(liter_lines + stylize("|", colored.fg("red")))

            directions = {"up": "↑", "down": "↓", "right": "→", "left": "←"}
            direction_arrow = directions.get(direction, "")
            direction = "   " + stylize(direction_arrow, colored.fg("green"))

            print(tops + stylize("+", colored.fg("red")) + direction)

            # next time, the board will be created when the move is done
            self.canCreateBoard = False

            self.printBestScore()
            self.printScore()
            self.printGameKeys()

    def printScore(self):
        print(
            stylize("Score = ", colored.fg("red"))
            + stylize("{}", colored.fg("red")).format(puzzle.__score)
        )

    def printBestScore(self):
        best_score = 0
        if self.__score > self.__best_score:
            best_score = self.__score
            with open("best-score.txt", "w") as bs:
                bs.write(str(best_score))
        else:
            best_score = self.__best_score
        print(
            stylize("Best Score =", colored.fg("red"))
            + stylize(" {}".format(best_score), colored.fg("yellow"))
        )

    def printGameKeys(self):
        print(
            stylize("↑ ← ↓ →", colored.fg("green"))
            + " or "
            + stylize("w a s d", colored.fg("green"))
        )


# START GAME
size = input(stylize("Enter puzzle size: ", colored.fg("red")))
puzzle = Puzzle(size)
puzzle.createBoard()
puzzle.canCreateBoard = False

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        move = event.name.lower()
        if move == "q":
            sys.exit()
        elif move == "up" or move == "w":
            # first move cells to fill blank cells if possible. then merge simillar celss if possible and then move again to fill blank cells that create after merge
            puzzle.moveUp()
            puzzle.mergeUp()
            puzzle.moveUp()
            puzzle.createBoard("up")
        elif move == "left" or move == "a":
            puzzle.moveLeft()
            puzzle.mergeLeft()
            puzzle.moveLeft()
            puzzle.createBoard("left")
        elif move == "down" or move == "s":
            puzzle.moveDown()
            puzzle.mergeDown()
            puzzle.moveDown()
            puzzle.createBoard("down")
        elif move == "right" or move == "d":
            puzzle.moveRight()
            puzzle.mergeRight()
            puzzle.moveRight()
            puzzle.createBoard("right")
        else:
            continue

        if not puzzle.canContinue():
            print(stylize("GAME OVER !!!", colored.fg("white") + colored.bg("red")))
            while True:
                continue_puzzle = input("continue puzzle? y/n: ")
                if continue_puzzle == "n":
                    print("good bye")
                    sys.exit()
                elif continue_puzzle == "y":
                    puzzle.resetGame()
                    puzzle.createBoard()
                    break
