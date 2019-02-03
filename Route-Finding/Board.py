# James Archbold & Nathan Griffiths, 2018.
# Coursework 2: Game Types 2 & 3

import random


class Space:
    # Space type will dictact the types of acceptable actions in each space.
    spaceTypeDict = {0: "Empty", 1: "Wall", 2: "Goal", 3: "Start", 4: "Object", 5: "Enemy"}

    def __init__(self, id):
        self.spaceType = id

    def scanSpace(self):
        return self.spaceType

    def idUpdate(self, newID):
        self.spaceType = newID

    def spaceEnv(self):
        return self.spaceTypeDict[self.spaceType]


class Board:
    def __init__(self, x, y):
        self.col = y
        self.row = x
        self.room = list()
        self.start = [0, 0]
        self.goal = [0, 0]
        self.totalItems = 0
        for i in range(x):
            self.room.append(list())
            for j in range(y):
                self.room[i].append(Space(0))

    def scanSpace(self, x, y):
        if x < 0 or y < 0:
            return "1"

        if x >= self.row or y >= self.col:
            return "1"

        return self.room[x][y].scanSpace()

    def getStart(self):
        return self.start

    def getGoal(self):
        return self.goal

    def spaceEnv(self, x, y):
        if x < 0 or y < 0:
            return "Wall"

        if x >= self.row or y >= self.col:
            return "Wall"

        return self.room[x][y].spaceEnv()

    def updateSpace(self, x, y, id):
        self.room[x][y].idUpdate(id)

    def wallBuilder(self, density, startSpace):

        maze = list()
        maze.append([0, startSpace])
        walls = list()

        walls.append(([1, startSpace], "r"))
        if startSpace != 0:
            walls.append(([0, startSpace - 1], "c"))

        if startSpace != self.col - 1:
            walls.append(([0, startSpace + 1], "c"))

        while len(walls) > 0:
            choice = random.randint(0, len(walls) - 1)
            wallCell = walls[choice][0]
            shift = walls[choice][1]

            if shift == "r":
                if [wallCell[0] - 1, wallCell[1]] not in maze:
                    maze.append([wallCell[0], wallCell[1]])
                    if wallCell[0] != 0:
                        maze.append([wallCell[0] - 1, wallCell[1]])

                        if wallCell[0] - 1 != 0:
                            walls.append(([wallCell[0] - 2, wallCell[1]], "r"))
                        if wallCell[1] != 0:
                            walls.append(([wallCell[0] - 1, wallCell[1] - 1], "c"))
                        if wallCell[1] != self.col - 1:
                            walls.append(([wallCell[0] - 1, wallCell[1] + 1], "c"))

                elif [wallCell[0] + 1, wallCell[1]] not in maze:
                    maze.append([wallCell[0], wallCell[1]])
                    if wallCell[0] != self.row - 1:
                        maze.append([wallCell[0] + 1, wallCell[1]])

                        if wallCell[0] + 1 != self.row - 1:
                            walls.append(([wallCell[0] + 2, wallCell[1]], "r"))
                        if wallCell[1] != 0:
                            walls.append(([wallCell[0] + 1, wallCell[1] - 1], "c"))
                        if wallCell[1] != self.col - 1:
                            walls.append(([wallCell[0] + 1, wallCell[1] + 1], "c"))

            elif shift == "c":
                if [wallCell[0], wallCell[1] - 1] not in maze:
                    maze.append([wallCell[0], wallCell[1]])
                    if wallCell[1] != 0:
                        maze.append([wallCell[0], wallCell[1] - 1])

                        if wallCell[1] - 1 != 0:
                            walls.append(([wallCell[0], wallCell[1] - 2], "c"))
                        if wallCell[0] != 0:
                            walls.append(([wallCell[0] - 1, wallCell[1] - 1], "r"))
                        if wallCell[0] != self.row - 1:
                            walls.append(([wallCell[0] + 1, wallCell[1] - 1], "r"))

                elif [wallCell[0], wallCell[1] + 1] not in maze:
                    maze.append([wallCell[0], wallCell[1]])
                    if wallCell[1] != self.col - 1:
                        maze.append([wallCell[0], wallCell[1] + 1])

                        if wallCell[1] + 1 != self.col - 1:
                            walls.append(([wallCell[0], wallCell[1] + 2], "c"))
                        if wallCell[0] != 0:
                            walls.append(([wallCell[0] - 1, wallCell[1] + 1], "r"))
                        if wallCell[0] != self.row - 1:
                            walls.append(([wallCell[0] + 1, wallCell[1] + 1], "r"))

            walls.remove(walls[choice])

        madeBlocks = 0
        for i in range(self.row):
            for j in range(self.col):
                if [i, j] not in maze:
                    self.room[i][j].idUpdate(1)
                    madeBlocks = madeBlocks + 1

        wallBlocks = int((self.col * self.row) * density)
        if madeBlocks < wallBlocks:
            madeBlocks = wallBlocks + 10

        while madeBlocks > wallBlocks:
            randRow = random.randint(0, self.row - 1)
            randCol = random.randint(0, self.col - 1)

            if self.scanSpace(randRow, randCol) == 1:
                checkWallList = (
                [randRow + 1, randCol], [randRow - 1, randCol], [randRow, randCol + 1], [randRow, randCol - 1])
                count = 0
                for [r, c] in checkWallList:
                    if self.scanSpace(r, c) != 1:
                        count = count + 1
                        break

                if count > 0:
                    self.room[randRow][randCol].idUpdate(0)
                    madeBlocks = madeBlocks - 1

        while True:
            randEnd = random.randint(0, self.col - 1)

            if self.scanSpace(self.row - 1, randEnd) == 0:
                self.room[self.row - 1][randEnd].idUpdate(2)
                self.goal = [self.row - 1, randEnd]
                break;

    def buildBoard(self, bType=1, density=0.2, items=0):

        if bType == 1:
            startSpace = random.randint(0, self.col - 1)
            self.room[0][startSpace].idUpdate(3)
            self.start = [0, startSpace]
            self.wallBuilder(density, startSpace)

        if bType == 2 or bType == 3:
            startSpace = random.randint(0, self.col - 1)
            self.room[0][startSpace].idUpdate(3)
            self.start = [0, startSpace]
            self.wallBuilder(density, startSpace)

            itemsPlaced = 0
            while itemsPlaced < items:
                randRow = random.randint(0, self.row - 1)
                randCol = random.randint(0, self.col - 1)

                if self.scanSpace(randRow, randCol) == 0:
                    self.room[randRow][randCol].idUpdate(4)
                    itemsPlaced = itemsPlaced + 1
            self.totalItems = items

    def boardprinter(self):
        rowList = list()

        for i in range(self.row):
            currentRow = "| "
            for j in range(self.col):
                currentRow = currentRow + str(self.room[i][j].scanSpace()) + " | "

            currentRow = currentRow
            rowList.append(currentRow)

        for g in range(len(rowList)):
            print(rowList[g])

    def writeBoard(self, fileName, enemyList=list()):
        import Enemy
        rowList = list()
        for i in range(self.row):
            currentRow = ""
            for j in range(self.col):
                currentRow = currentRow + str(self.room[i][j].scanSpace()) + ","

            currentRow = currentRow[:len(currentRow) - 1]
            rowList.append(currentRow)

        with open(fileName, "a") as f:
            f.write(str(self.row) + "\n")
            f.write(str(self.col) + "\n")
            for g in range(len(rowList)):
                f.write(rowList[g] + "\n")

            if len(enemyList) > 0:
                for i in range(len(enemyList)):
                    enString = "[" + str(enemyList[i].tactic) + ", " + str(enemyList[i].currRow) + ", " + str(
                        enemyList[i].currCol)

                    if len(enemyList[i].squares) > 0:
                        for j in range(len(enemyList[i].squares)):
                            [xx, yy] = enemyList[i].squares[j]
                            enString = enString + "," + str(xx) + ", " + str(yy)
                    enString = enString + "]\n"
                    f.write(enString)

            f.write("================\n")

    def readBoard(self, fileName):
        import Enemy
        rowList = list()
        lineNum = 0
        enList = list()

        with open(fileName) as f:
            for line in f:

                if lineNum == 0:
                    self.row = int(line)
                    lineNum = 1
                elif lineNum == 1:
                    self.col = int(line)
                    lineNum = 2
                elif '================' in line:
                    self.room = rowList
                    break
                elif '[' in line:
                    self.room = rowList
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    chars = line.split(",")
                    tact = chars[0]
                    [xx, yy] = [int(chars[1]), int(chars[2])]
                    squareList = list()
                    d = 3
                    if len(chars) > 3:
                        while len(chars) > d:
                            cX = int(chars[d])
                            d = d + 1
                            cY = int(chars[d])
                            d = d + 1
                            squareList.append([cX, cY])

                    en = Enemy.Enemy(self, startRow=xx, startCol=yy, tactic=tact, squares=squareList)
                    enList.append(en)
                else:
                    row = line.strip("\n")
                    row = row.split(",")
                    spaceList = list()

                    for i in range(len(row)):
                        spaceList.append(Space(int(row[i])))

                    rowList.append(spaceList)

        itemsFound = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.room[i][j].scanSpace() == 2:
                    self.goal = [i, j]
                elif self.room[i][j].scanSpace() == 3:
                    self.start = [i, j]
                elif self.room[i][j].scanSpace() == 4:
                    itemsFound = itemsFound + 1

        self.totalItems = itemsFound
        return enList
