# James Archbold & Nathan Griffiths, 2018.
# Coursework 2: Game Types 2 & 3

import Board
import random
import Enemy
from importlib import import_module


class Game:

    def __init__(self, gameType=1, rows=20, cols=20, density=0.2, file="", items=0, eTups=list()):
        self.gameType = gameType
        self.rows = rows
        self.cols = cols
        self.density = density
        self.collisions = 0
        self.movesMade = 0
        self.board = Board.Board(self.rows, self.cols)
        self.carrying = False
        self.totalItems = items
        self.itemsRetrieved = 0
        self.enemyList = list()
        self.enemyCollisions = 0

        if file != "":
            self.enemyList = self.board.readBoard(file)
            self.cols = self.board.col
            self.rows = self.board.row
            self.totalItems = self.board.totalItems
        else:
            self.board.buildBoard(bType=self.gameType, density=density, items=items)

            if gameType == 3:
                for i in range(len(eTups)):
                    tact = eTups[i][0]
                    start = eTups[i][1]
                    if len(eTups[i]) > 2:
                        moves = eTups[2]

                    en = Enemy.Enemy(self.board, startRow=start[0], startCol=start[1], tactic=tact, squares=moves)
                    self.board.updateSpace(start[0], start[1], 5)
                    self.enemyList.append(en)

        self.currentRow, self.currentCol = self.board.getStart()

    def addEnemy(self, enemy):
        self.enemyList.append(enemy)
        self.board.updateSpace(enemy.currRow, enemy.currCol, 5)

    def atGoal(self):
        if self.board.scanSpace(self.currentRow, self.currentCol) == 2:
            return True
        else:
            return False

    def numberOfObjs(self):
        return self.totalItems

    def moveRobot(self, direction, verbose="False"):
        if direction == "WEST":
            row = self.currentRow
            col = self.currentCol - 1
            if verbose:
                print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moving " + str(direction) + ".")
            if col == -1:
                if verbose:
                    print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                self.collisions = self.collisions + 1
                self.movesMade = self.movesMade + 1
                col = self.currentCol
            else:
                if self.board.scanSpace(row, col) == 1:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                    self.collisions = self.collisions + 1
                    self.movesMade = self.movesMade + 1
                    col = self.currentCol
                elif self.board.scanSpace(row, col) == 5:
                    if verbose:
                        print("Current Space: " + str(
                            (self.currentRow, self.currentCol)) + ". You've collided with an enemy! How unfortunate.")

                    if self.carrying:
                        self.carrying = False
                        if verbose:
                            print("Current Space: " + str(
                                (self.currentRow, self.currentCol)) + ". The enemy took the object away from you!")

                    self.enemyCollisions = self.enemyCollisions + 1
                    self.movesMade = self.movesMade + 1
                else:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moved " + str(
                            direction) + " successfully.")
                    self.movesMade = self.movesMade + 1

            self.currentRow = row
            self.currentCol = col

        elif direction == "EAST":
            row = self.currentRow
            col = self.currentCol + 1
            if verbose:
                print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moving " + str(direction) + ".")
            if col == self.cols:
                if verbose:
                    print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                self.collisions = self.collisions + 1
                self.movesMade = self.movesMade + 1
                col = self.currentCol
            else:
                if self.board.scanSpace(row, col) == 1:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                    self.collisions = self.collisions + 1
                    self.movesMade = self.movesMade + 1
                    col = self.currentCol
                elif self.board.scanSpace(row, col) == 5:
                    if verbose:
                        print("Current Space: " + str(
                            (self.currentRow, self.currentCol)) + ". You've collided with an enemy! How unfortunate.")

                    if self.carrying:
                        self.carrying = False
                        if verbose:
                            print("Current Space: " + str(
                                (self.currentRow, self.currentCol)) + ". The enemy took the object away from you!")

                    self.enemyCollisions = self.enemyCollisions + 1
                    self.movesMade = self.movesMade + 1
                else:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moved " + str(
                            direction) + " successfully.")
                    self.movesMade = self.movesMade + 1

            self.currentRow = row
            self.currentCol = col

        elif direction == "NORTH":
            row = self.currentRow - 1
            col = self.currentCol
            if verbose:
                print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moving " + str(direction) + ".")
            if row == -1:
                if verbose:
                    print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                self.collisions = self.collisions + 1
                self.movesMade = self.movesMade + 1
                row = self.currentRow
            else:
                if self.board.scanSpace(row, col) == 1:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                    self.collisions = self.collisions + 1
                    self.movesMade = self.movesMade + 1
                    row = self.currentRow
                elif self.board.scanSpace(row, col) == 5:
                    if verbose:
                        print("Current Space: " + str(
                            (self.currentRow, self.currentCol)) + ". You've collided with an enemy! How unfortunate.")

                    if self.carrying:
                        self.carrying = False
                        if verbose:
                            print("Current Space: " + str(
                                (self.currentRow, self.currentCol)) + ". The enemy took the object away from you!")

                    self.enemyCollisions = self.enemyCollisions + 1
                    self.movesMade = self.movesMade + 1
                else:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moved " + str(
                            direction) + " successfully.")
                    self.movesMade = self.movesMade + 1

            self.currentRow = row
            self.currentCol = col

        elif direction == "SOUTH":
            row = self.currentRow + 1
            col = self.currentCol
            if verbose:
                print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moving " + str(direction) + ".")
            if row == self.rows:
                if verbose:
                    print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                self.collisions = self.collisions + 1
                self.movesMade = self.movesMade + 1
                row = self.currentRow
            else:
                if self.board.scanSpace(row, col) == 1:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". OWCH. Hit a wall.")
                    self.collisions = self.collisions + 1
                    self.movesMade = self.movesMade + 1
                    row = self.currentRow
                elif self.board.scanSpace(row, col) == 5:
                    if verbose:
                        print("Current Space: " + str(
                            (self.currentRow, self.currentCol)) + ". You've collided with an enemy! How unfortunate.")

                    if self.carrying:
                        self.carrying = False
                        if verbose:
                            print("Current Space: " + str(
                                (self.currentRow, self.currentCol)) + ". The enemy took the object away from you!")

                    self.enemyCollisions = self.enemyCollisions + 1
                    self.movesMade = self.movesMade + 1
                else:
                    if verbose:
                        print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Moved " + str(
                            direction) + " successfully.")
                    self.movesMade = self.movesMade + 1

            self.currentRow = row
            self.currentCol = col

        elif direction == "GRAB":
            if self.board.scanSpace(self.currentRow, self.currentCol) == 4:
                if self.carrying:
                    if verbose:
                        print("Current Space: " + str(
                            (self.currentRow, self.currentCol)) + ". Cannot pick up more than one object at once.")
                else:
                    self.carrying = True
                    self.board.updateSpace(self.currentRow, self.currentCol, 0)
                    if verbose:
                        print("Current Space: " + str(
                            (self.currentRow, self.currentCol)) + ". Object has been collected.")
            else:
                if verbose:
                    print(
                        "Current Space: " + str((self.currentRow, self.currentCol)) + ". There is nothing to pick up.")

            self.movesMade = self.movesMade + 1

        elif direction == "DROP":
            if not self.carrying:
                if verbose:
                    print("Current Space: " + str((self.currentRow, self.currentCol)) + ". There is nothing to drop.")
            else:
                if self.board.scanSpace(self.currentRow, self.currentCol) != 2 and self.board.scanSpace(self.currentRow,
                                                                                                        self.currentCol) != 1:
                    self.board.updateSpace(self.currentRow, self.currentCol, 4)
                    self.carrying = False
                    if verbose:
                        print(
                            "Current Space: " + str((self.currentRow, self.currentCol)) + ". Object has been dropped.")
                elif self.board.scanSpace(self.currentRow, self.currentCol) == 2:
                    self.carrying = False
                    self.itemsRetrieved = self.itemsRetrieved + 1
                    if verbose:
                        print("Current Space: " + str((self.currentRow,
                                                       self.currentCol)) + ". Object has been successfully delivered to the goal.")
            self.movesMade = self.movesMade + 1
        elif direction == "WAIT":
            if verbose:
                print("Current Space: " + str((self.currentRow, self.currentCol)) + ". Paitently waiting.")
        else:
            raise ValueError(
                "Only the following values for direction can be accepted: NORTH, SOUTH, EAST, WEST, GRAB, DROP, WAIT.")

    def moveEnemyRobots(self, verbose=False):
        for en in self.enemyList:
            [currx, curry] = [en.currRow, en.currCol]
            [newx, newy] = en.nextMove()
            self.board.updateSpace(currx, curry, 0)
            self.board.updateSpace(newx, newy, 5)

            if [self.currentRow, self.currentCol] == [newx, newy]:
                if verbose:
                    print("Current Space: " + str(
                        (self.currentRow, self.currentCol)) + ". An enemy ran into you! How devious.")

                if self.carrying:
                    self.carrying = False
                    if verbose:
                        print("Current Space: " + str(
                            (self.currentRow, self.currentCol)) + ". The enemy took the object away from you!")

                self.enemyCollisions = self.enemyCollisions + 1

    def getRowNumber(self):
        if self.gameType < 3:
            return self.rows
        else:
            return 0

    def getColNumber(self):
        if self.gameType < 3:
            return self.cols
        else:
            return 0

    def getGoal(self):
        return self.board.getGoal()

    def getStart(self):
        return self.board.getStart()

    def scanSpace(self, x, y):
        if self.gameType < 3:
            return self.board.spaceEnv(x, y)
        elif abs(self.currentRow - x) < 10 and abs(self.currentCol - y) < 10:
            return self.board.spaceEnv(x, y)
        else:
            return "Error"

    def getCurrentLocation(self):
        return [self.currentRow, self.currentCol]

    def getEnemyPath(self, x, y):
        if self.scanSpace(x, y) == "Enemy":
            for i in range(len(self.enemyList)):
                en = self.enemyList[i]
                if en.tactic == "predefined-known" and en.currRow == x and en.currCol == y:
                    return en.squares

        return "Error"

    def robotCarrying(self):
        return self.carrying

    def setMoveList(self, moveList):
        self.moveList = moveList

    def playGame(self, robot, verbose=False, module="Robot"):
        moduleObj = import_module(module)
        classObj = getattr(moduleObj, "Robot")
        print("Starting in Space: " + str([self.currentRow, self.currentCol]))
        if self.gameType == 1:
            nextMove = ""
            while nextMove != "STOP":
                nextMove = robot.nextMove(self, self.gameType)
                if nextMove != "STOP":
                    self.moveRobot(nextMove, verbose=verbose)

            if self.atGoal():
                print(str(robot.name) + " has successfully navigated the terrain!")
                print("Moves made: " + str(self.movesMade))
                print("Collisions: " + str(self.collisions))
                return True
            else:
                print(str(robot.name) + " did not reach the goal.")
                print("Moves made: " + str(self.movesMade))
                print("Collisions: " + str(self.collisions))
                return False

        elif self.gameType == 2:
            nextMove = ""
            while nextMove != "STOP":
                nextMove = robot.nextMove(self, self.gameType)
                if nextMove != "STOP":
                    self.moveRobot(nextMove, verbose=verbose)

            if self.atGoal():
                print(str(robot.name) + " has successfully navigated the terrain!")
                print("Moves made: " + str(self.movesMade))
                print("Collisions: " + str(self.collisions))
                print("Retrieved " + str(self.itemsRetrieved) + " out of " + str(self.totalItems))
                return True
            else:
                print(str(robot.name) + " did not reach the goal.")
                print("Moves made: " + str(self.movesMade))
                print("Collisions: " + str(self.collisions))
                print("Retrieved " + str(self.itemsRetrieved) + " out of " + str(self.totalItems))
                return False

        elif self.gameType == 3:
            nextMove = ""
            while nextMove != "STOP":
                nextMove = robot.nextMove(self, self.gameType)
                print("Next move will be: " + str(nextMove))
                if nextMove != "STOP":
                    print("Moving robot")
                    self.moveRobot(nextMove, verbose=verbose)
                    print("Moving Enemy")
                    self.moveEnemyRobots(verbose=verbose)

            if self.atGoal():
                print(str(robot.name) + " has successfully navigated the terrain!")
                print("Moves made: " + str(self.movesMade))
                print("Collisions: " + str(self.collisions))
                print("Enemy Collisions: " + str(self.enemyCollisions))
                print("Retrieved " + str(self.itemsRetrieved) + " out of " + str(self.totalItems))
                return True
            else:
                print(str(robot.name) + " did not reach the goal.")
                print("Moves made: " + str(self.movesMade))
                print("Collisions: " + str(self.collisions))
                print("Enemy Collisions: " + str(self.enemyCollisions))
                print("Retrieved " + str(self.itemsRetrieved) + " out of " + str(self.totalItems))
                return False
