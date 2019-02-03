# James Archbold & Nathan Griffiths, 2018.
# Coursework 2: Game Types 2 & 3

import Search
import Enemy
import random
import Board
import Robot

# Coursework 2: Game Types 2 & 3 - Complex route finding.

# You are provided with some example mazes for testing.
# Simply uncomment the mazeFile definition that you wish to use.
# Note that these are not the mazeFile definitions that will be used for marking.

#Game Type 2 - Retrieval Task
# [gT, mazeFile] = [2, "exampleMazes/GameType2/10Squares.txt"] #This maze can be completed in 78 moves.
# [gT, mazeFile] = [2, "exampleMazes/GameType2/25Squares.txt"] #This maze can be completed in 463 moves.
# [gT, mazeFile] = [2, "exampleMazes/GameType2/75Squares.txt"] #This maze can be completed in 10046 moves.
# [gT, mazeFile] = [2, "exampleMazes/GameType3/512SquaresGameType2.txt"]

#Game Type 3 - Retrieval and Avoidance Task
# [gT, mazeFile] = [3, "exampleMazes/GameType3/10Squares-ARGS.txt"] #Maze contains an aggressive enemy that will guard a particular point. A very good solution will complete this maze in ~150 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/10Squares-PDFK.txt"] #Maze contains an enemy that moves in a predefined path, that you can access. A very good solution will complete this maze in ~130 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/10Squares-PDFU.txt"] #Maze contains an enemy that moves in a predefined path, that you cannot access. A very good solution will complete this maze in ~130 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/10Squares-RNDM.txt"] #Maze contains an enemy that moves in a random path. A very good solution will complete this maze in ~100 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/50Squares-ARGS.txt"] #Maze contains multiple aggressive enemies that will guard particular points. A very good solution will complete this maze in ~2800 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/50Squares-PDFK.txt"] #Maze contains multiple enemies that move in a predefined path, that you can access. A very good solution will complete this maze in ~3000 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/50Squares-PDFU.txt"] #Maze contains multiple enemies that move in a predefined path, that you cannot access. A very good solution will complete this maze in ~3800 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/50Squares-RNDM.txt"] #Maze contains multiple enemies that move in a random path. A very good solution will complete this maze in ~3300 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/50Squares40DensityMultiMEn0.txt"] #Maze contains multiple types of enemies. A very good solution will complete this maze in ~2400 moves.
# [gT, mazeFile] = [3, "exampleMazes/GameType3/512SquaresGameType2.txt"]
# g = Search.Game(gameType=gT, file=mazeFile)

# Alternatively, you can create your own maze, using the command given below.
# gameType = 1, 2 or 3 (use 2 and 3 Coursework 2).
# rows = number of rows you want the board to have
# cols = number of columns you want the board to have
# density = Approximately how much of the board will be walls. A density of 0 is no walls. Becomes less guaranteed above 0.5.
# file = if you have a text file with a maze in it, you can load it.
# items = the number of objects to be retrieved that you want placed in the board.
# eTups = Tuples to describe any enemies. This only needed for gameType 3. Enemies can also be added by using g.addEnemy(enemy)
#
#An enemy tuple consists of: (tact, [x,y], [x0,y0], [x1,y1], ..., [xn,yn])
#tact = a string describing the tactic of the enemy. Must be from the following list: ["predefined-known", "predefined-unknown", "random", "aggressive"]
#[x,y] = The starting row (x) and column (y) of the enemy.
#[x0,y0],...,[xn,yn] = Optional arguments that provide the set of spaces the enemy will move to. Typically, this list will start and end at the same square. This argument is only used for robots with the 'predefined' behaviour types.
#
#If you wish to make an enemy object and add using g.addEnemy(en) you can do so as follows:
# en = Enemy.Enemy(gameBoard, startRow=0, startCol=0, tactic="predefined-known", squares=list())
#gameBoard can be accessed with g.board
#startRow and startCol are the starting positions of the enemy
#tactic is a string describing the robot's behaviour
#squares is a list of co-ordinates, [x,y], describing the order of squares that the robot is expected to visit. Again, typically this list starts and ends at the same place.
#Make sure enemies start on a square that is not already occupied by something. A board space can be scanned using 'g.board.spaceEnv(x,y)'.
#
# g = Search.Game(gameType=1, rows=20, cols=20, density=0.2, file="", items=0, eTups=list())
# g = Search.Game(gameType=gT, file=mazeFile)
# You can visualise the board using the following method call
# g.board.boardprinter()

# roboInstance = Robot.Robot()
# g.playGame(roboInstance, verbose=False)
# g.playGame(roboInstance, verbose=True)

games = 10

i = 1
collisions = []
moves = []
objects = []
while i <= games:
    print("Game ", i)
    g = Search.Game(gameType=gT, file=mazeFile)
    roboInstance = Robot.Robot()
    g.playGame(roboInstance, verbose=False)
    collisions.append(g.enemyCollisions)
    moves.append(g.movesMade)
    objects.append(g.itemsRetrieved)

    i += 1
print("EXIT REPORT")
print()
print("Played ",i-1," games.")
print("ENEMY COLLISIONS")
print("Most collisions: ", max(collisions)," (Game ",collisions.index(max(collisions)) + 1,")")
print("Least collisions: ", min(collisions)," (Game ",collisions.index(min(collisions)) + 1,")")
print("Total collisions: ", sum(collisions))
print("OBJECTS")
print("Most objects: ", max(objects)," (Game ",objects.index(max(objects)) + 1,")")
print("Least objects: ", min(objects)," (Game ",objects.index(min(objects)) + 1,")")
print("Total objects: ", sum(objects))
print("MOVES")
print("Most moves: ", max(moves)," (Game ",moves.index(max(moves)) + 1,")")
print("Least moves: ", min(moves)," (Game ",moves.index(min(moves)) + 1,")")
print("Total moves: ", sum(moves))