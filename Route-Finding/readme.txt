The files in this .zip contain all the required Python files for you to develop a solution to CS255 Artificial Intelligence Coursework 2, which builds on Coursework 1.

Of the 5 files, your main focus will be Robot.py, which is where you will create your search strategy for this coursework. The nextMove() method in the Robot class is where you should put your solution. Currently, so that you can run the coursework, it simply returns a random list of moves. 

There is a detailed preamble in Robot.py that covers the methods you are permitted to use from other files, and the basics of the game environment. It also lists submission instructions for your code, namely that you should submit a single .py file that contains a definition for the Robot class, with your nextMove() method. The name of your submitted file must be "your-uni-ID-number.py" (with no letters), e.g., "1001234.py". Instructions for the report are in the coursework handout.

The other file that you will use in this coursework is runMaze.py.  This file allows you to test your robot and its nextMove() method, using a variety of mazes. The preamble in runMaze.py details how to use it to run the pre-made mazes and the necessary steps to create your own mazes if you wish. Your submission will be marked using a selection of environments which have same the form as those in the exampleMazes directory. 

Note that while developing your solution, you may wish to use some of the functions found in other provided coursework files for debugging purposes. This is fine, but your submitted solution must ONLY contain APPROVED methods, as detailed in the preamble of Robot.py. Permitted imports are restricted to the use of math and random functions, and YOU MUST NOT IMPORT ANY OTHER LIBRARIES OR FUNCTIONS.

In addition to Robot.py and runMaze.py the coursework .zip contains the following files:

Board.py - contains the Space and Board classes. The Board class includes methods to create mazes according to the different game types (game types 2 & 3 are relevant for Coursework 2), access the start and goal locations, return a space's type, read a board from a text file, write a board to a text file and print a board to the command line.  The Space class represents a place on the board, and stores the type of space (empty, wall, goal, start, object, enemy). You should not need to use any of the methods in this file, and your solution must only make use of the permitted methods as detailed in the preamble of Robot.py.

Enemy.py - Defines an enemy robot in the maze, including the strategy they use to move. An enemy robot can have one of several types of strategy, and this is determined on creation. Again, your solution should not contain any reference to this file. 

Search.py - This file contains the Game class and defines how the robot can interact with the board. This class is the one that runs the game, calling your robot for its next move. It then interprets these moves and updates the game state appropriately. There are a variety of utility methods in this class, several of which you are allowed to make use of in your solution, as detailed in the preamble of Robot.py. Notably, you can access the location of the start and goal, your current location, the type of space a given coordinate contains, the number of rows and columns in the board, the number of objects to find in the board, the path of a particular enemy type and whether your robot is currently carrying an object. Note that some of these methods work different for game type 3 due to partial information.

It is strongly suggested that you avoid editing any file other than runMaze.py and Robot.py. The versions of the Board.py and Search.py provided to you are identical to the ones that will be used in marking this coursework. If you edit these, and your solution requires the edited versions, your solution will not work and you will receive 0 marks for its functionality. 

