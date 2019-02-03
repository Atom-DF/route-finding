# James Archbold & Nathan Griffiths, 2018.
# Coursework 2: Game Types 2 & 3

import Board
import random


class Enemy:
    def __init__(self, gameBoard, startRow=0, startCol=0, tactic="predefined-known", squares=list()):
        self.currRow = startRow
        self.currCol = startCol
        self.board = gameBoard
        self.tactic = tactic
        self.squares = squares
        self.currentMoveIndex = 0

        if len(squares) == 0:
            if self.tactic == "predefined-known" or self.tactic == "predefined-unknown":
                self.squares = self.preDefTact()

        if tactic == "aggressive":
            self.aggPrep()

    def aggPrep(self):
        potentialTargets = list()

        for i in range(self.board.row):
            for j in range(self.board.col):
                if self.board.scanSpace(i, j) == 2 or self.board.scanSpace(i, j) == 4:
                    potentialTargets.append((i, j))

        (self.gx, self.gy) = potentialTargets[random.randint(0, len(potentialTargets) - 1)]

        self.nearTarget = False

    def preDefTact(self):
        squareList = list()
        squareList.append([self.currRow, self.currCol])
        numOfMoves = random.randint(5, self.board.row)
        modifiers = [-1, 1]
        movesSaved = 0

        lastRow = self.currRow
        lastCol = self.currCol
        attempts = 0
        while movesSaved < numOfMoves and attempts < 100:
            rowOrCol = random.randint(0, 1)

            if rowOrCol:
                newCol = lastCol + modifiers[random.randint(0, 1)]

                if self.board.scanSpace(lastRow, newCol) == 0:
                    squareList.append([lastRow, newCol])
                    movesSaved = movesSaved + 1
                    lastCol = newCol

            else:
                newRow = lastRow + modifiers[random.randint(0, 1)]

                if self.board.scanSpace(newRow, lastCol) == 0:
                    squareList.append([newRow, lastCol])
                    movesSaved = movesSaved + 1
                    lastRow = newRow

            attempts = attempts + 1

        rSquares = squareList[::-1]
        rSquares.pop(0)

        for i in range(len(rSquares)):
            squareList.append(rSquares[i])

        return squareList

    def randomMove(self):
        lastRow = self.currRow
        lastCol = self.currCol
        modifiers = [-1, 1]
        attempts = 0
        while attempts < 100:
            rowOrCol = random.randint(0, 1)

            if rowOrCol:
                newCol = lastCol + modifiers[random.randint(0, 1)]

                if self.board.scanSpace(lastRow, newCol) == 0:
                    move = [lastRow, newCol]
                    return move

            else:
                newRow = lastRow + modifiers[random.randint(0, 1)]

                if self.board.scanSpace(newRow, lastCol) == 0:
                    move = [newRow, lastCol]
                    return move

            attempts = attempts + 1

        return [lastRow, lastCol]

    def nextMove(self):
        if self.tactic == "predefined-known" or self.tactic == "predefined-unknown":
            move = self.squares[self.currentMoveIndex]
            if self.board.scanSpace(move[0], move[1]) != 0:
                move = [self.currRow, self.currCol]
            self.currentMoveIndex = (self.currentMoveIndex + 1) % len(self.squares)
            self.currRow = move[0]
            self.currCol = move[1]
            return move

        elif self.tactic == "random":
            move = self.randomMove()
            self.currRow = move[0]
            self.currCol = move[1]
            return move

        elif self.tactic == "aggressive":
            if not self.nearTarget:

                rowOrCol = random.randint(0, 1)

                if rowOrCol:
                    modifier = 0
                    if self.currCol - self.gy < 0:
                        modifier = 1
                    else:
                        modifier = -1

                    if self.board.scanSpace(self.currRow, self.currCol + modifier) == 0:
                        move = [self.currRow, self.currCol + modifier]
                    else:
                        move = self.randomMove()

                else:
                    modifier = 0
                    if self.currRow - self.gx < 0:
                        modifier = 1
                    else:
                        modifier = -1

                    if self.board.scanSpace(self.currRow + modifier, self.currCol) == 0:
                        move = [self.currRow + modifier, self.currCol]
                    else:
                        move = self.randomMove()

                if move[0] in range(self.gx - 3, self.gx + 3) and move[1] in range(self.gy - 3, self.gy + 3):
                    self.nearTarget = True

                self.currRow = move[0]
                self.currCol = move[1]
                return move

            else:

                move = [self.gx + 10, self.gy + 10]
                attempts = 0
                while (move[0] not in range(self.gx - 3, self.gx + 3) or move[1] not in range(self.gy - 3,
                                                                                              self.gy + 3)) and attempts < 100:
                    move = self.randomMove()
                    attempts = attempts + 1

                self.currRow = move[0]
                self.currCol = move[1]
                return move
