# James Archbold & Nathan Griffiths, 2018.
# Coursework 2: Game Types 2 & 3

import Search
import math
import random

# For this coursework I used two algorithms, A* and dijkstra's. These where slightly modified to fit the coursework.
# Again all the code is commented to explain how i implemented the broad algorithm of solving the two gametypes.
#
# For gametype 2, the gist of it is getting a path from goal to all items and a path from start to all items and combining one of the latter
# with a combination of the rest. This is because once you reach the goal for the first time you always come back to it to drop an item or stop the game.
#
#For gametype 3, the algorithm was quite similar except yit had to be an online search, so it still uses A* to find all paths.
# It stores and updates its storage depending on its surrounding, and so builds its own map of the environment and uses that
# to navigate through the env. The second part of it is avoiding enemies, I chose to favour recalculating a path if there is one
# instead of trying to wait to see if an opening can be made. This means the robot only tries to go to the object once (as in if
# the path is totally blocke and no other path to it is available then it will give up with this item).
#
# For a more detailed explanation of the Algorithms used, see the report provided.


class Robot:
	def __init__(self, name = "Robot"):
		self.name = name
		# The list of moves required from start to finish to solve the maze
		self.solution = []
		# The list of moves used for Gametype 3 when you need to explore the maze
		self.explore_path = []
		# Stores the cardinal directions
		self.directions = {(-1, 0): "NORTH", (1, 0): "SOUTH", (0, -1): "WEST", (0, 1): "EAST", (1, 1): "STOP", (0, 0): "WAIT",}
		# List of items to go fetch
		self.items = []
		# The total number of items discovered by the robot
		self.num_items = 0
		# The current item which needs to be fetched
		self.curr_item = None
		# The map of the env
		self.graph_origin = {}
		# The map which stores the center of 7*7 tiles which unable the robot to explore the maze
		self.explore_tile = {}
		# The list of enemies close by
		self.enemies = []
		# number of waits in a row
		self.tries = 0

	# return the string which corresponds to the opposite
	# direction to go from current to its origin
	# going from end to start
	def direction(self, start, end):
		return self.directions[(start[0] - end[0], start[1] - end[1])]

	# Calculate the distance from the current tile to the goal
	@staticmethod
	def heuristic(a, b):
		return abs(a[0] - b[0]) + abs(a[1] - b[1])

	# Get all the neighbors which aren't a wall or an out of bound tile
	@staticmethod
	def neighbors(game_env, current):
		temp = []
		# look for all the 4 possibilities
		for node_next in ((current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1),
						  (current[0], current[1] - 1)):
			if game_env.scanSpace(node_next[0], node_next[1]) != "Wall":
				temp.append(node_next)
		return temp

	# Calculates the minimum path to all attainable nodes from "start"
	def dijkstra(self, game_env, start):
		# Stores discovered tiles which aren't processed
		border = {(start[0], start[1]): 0}
		# Stores the tile explored before the one in the
		# key, by taking the value of any explored tile
		# and using it as key repeatedly you will always
		# find the shortest path back to the start
		origin = {(start[0], start[1]): None}
		# Stores the cost of moving to this tile from the start tile
		cost_so_far = {(start[0], start[1]): 0}

		# Go through the maze while there are unexplored tiles in border
		while len(border):
			# Get the next tile with the smallest value to process from border
			current = list(border.keys())[list(border.values()).index(min(border.values()))]
			# Pop the current tile off of border to avoid processing it again
			border.pop(current)
			if game_env.scanSpace(current[0], current[1]) == "Object" and start == tuple(game_env.getGoal()):
				self.items.append(current)
			# Discover each neighbors of current tile
			for node_next in self.neighbors(game_env, current):
				# this is unweighted so the cost is always 1
				new_cost = cost_so_far[current] + 1
				# Checks if the tile is undiscovered or if there is a faster route to this tile
				if node_next not in cost_so_far or new_cost < cost_so_far[node_next]:
					# update the cost or store it for this tile
					cost_so_far[node_next] = new_cost
					# Add the tile to border and calculate its priority, the closer it
					# is to the goal the smaller the heuristic is
					border[node_next] = new_cost
					origin[node_next] = current
		# This is to make sure we aren't overwriting the map when calling dijkstra to calculate the first item
		if start == tuple(game_env.getGoal()):
			self.graph_origin = origin
		# returns the map of the costs to get there from the "start"
		return cost_so_far

	# this uses A* to find the path to the first node
	def go_to_first(self, game_env, goal):
		# Gets the start tile
		start = game_env.getCurrentLocation()
		# Stores discovered tiles which aren't processed
		border = {(start[0], start[1]): 0}
		# Stores the tile explored before the one in the
		# key, by taking the value of any explored tile
		# and using it as key repeatedly you will always
		# find the shortest path back to the start
		origin = {(start[0], start[1]): None}
		# Stores the cost of moving to this tile from the start tile
		cost_so_far = {(start[0], start[1]): 0}
		# Go through the maze while there are unexplored tiles in border
		while len(border):
			# Get the next tile with the smallest value to process from border
			current = list(border.keys())[list(border.values()).index(min(border.values()))]
			# Pop the current tile off of border to avoid processing it again
			border.pop(current)
			# Found the goal so we can stop the search
			if current == goal:
				break
			# Discover each neighbors of current tile
			for node_next in self.neighbors(game_env, current):
				# this is unweighted so the cost is always 1
				new_cost = cost_so_far[current] + 1
				# Checks if the tile is undiscovered or if there is a faster route to this tile
				if node_next not in cost_so_far or new_cost < cost_so_far[node_next]:
					# update the cost or store it for this tile
					cost_so_far[node_next] = new_cost
					# Add the tile to border and calculate its priority, the closer it
					# is to the goal the smaller the heuristic is
					priority = new_cost + self.heuristic(goal, node_next)
					border[node_next] = priority
					origin[node_next] = current

		# Get the path from the goal to the start
		current = goal
		# go through the whole path and add it to the solutions list
		while current is not None:
			# Checks if the robot made it to the exit
			if not ((current[0], current[1]) in origin):
				self.solution.append("GRAB")
				break
			# Fetch the opposite direction in order to
			# come to the current tile from the previous one
			tmp = self.direction((current[0], current[1]),
								 origin[(current[0], current[1])])
			# Add it to the solution
			self.solution.insert(0, tmp)
			# set the new current tile to be the origin of the old current tile
			current = origin[(current[0], current[1])]
			# Add the final STOP instruction
			if origin[(current[0], current[1])] is None:
				self.solution.append("GRAB")
				break

	# Use the stored map to calculate paths to and from the goal
	def go_to(self, node, action):
		temp = []
		# go through the whole path and add it to the solutions list
		while node is not None:
			# Checks if the robot made it to the exit
			if not ((node[0], node[1]) in self.graph_origin):
				temp.append(action)
				break
			# Depending on the direction you take (towards or away from the goal)
			# you need to reverse the directions from the stored map and the order in which they show up
			if action in ["DROP", "STOP"]:
				tmp = self.direction(self.graph_origin[(node[0], node[1])], (node[0], node[1]))
				if action == "DROP":
					temp.append(tmp)
			else:
				tmp = self.direction((node[0], node[1]), self.graph_origin[(node[0], node[1])])
				temp.insert(0, tmp)

			# set the new current tile to be the origin of the old current tile
			node = self.graph_origin[(node[0], node[1])]
			# Add the final STOP instruction
			if self.graph_origin[(node[0], node[1])] is None:
				temp.append(action)
				break
		# Add it to the solution
		self.solution.extend(temp)

	# Calculate the first item to fetch
	def find_first_item(self, game_env, costs_goal):
		# This stores the coordinates of the first node to travel to
		curr = None
		# this stores the minimum cost of the first node
		temp = None
		# get the costs to travel to everynode from the start
		costs_start = self.dijkstra(game_env, tuple(game_env.getStart()))
		# go through all the items
		for n in self.items:
			# calculate the diference between these two distances to find the first node to travel to
			temp2 = costs_start[n] - costs_goal[n]
			# update the possible first node
			if temp is None or temp > temp2:
				temp = temp2
				curr = n
		# return first node
		return curr

	# Handles the logic, uses all other gametype 2 related methods to solve the maze
	def next_move2(self, game_env):
		# Check if it knows where to go
		if len(self.solution) > 0:
			# continue on the calculated path
			return self.solution.pop(0)
		# check if it is possible to find the exit from the start
		# dijkstra also finds all attainable items
		costs = self.dijkstra(game_env, tuple(game_env.getGoal()))
		# If there are items the robot can fetch
		if len(self.items) > 0:
			# Calculate which item to go to first from the start
			item = self.items.pop(self.items.index(self.find_first_item(game_env, costs)))
			# store the path from start to item
			self.go_to_first(game_env, item)
			# store the path from item to goal
			self.go_to(item, "DROP")
			# go through all the items
			for item in self.items:
				# store the path to go to the item
				self.go_to(item, "GRAB")
				# store the path to go to the goal
				self.go_to(item, "DROP")
		# no items are attainable go to goal
		elif tuple(game_env.getStart()) in costs:
			# store the path from start to goal
			self.go_to(tuple(game_env.getStart()), "STOP")
		# Add the final instruct to stop the robot, this also stops the robot when the goal is unattainable
		self.solution.append("STOP")
		# return the first instruction
		return self.solution.pop(0)

	# Store the robots' surroundings
	def store(self, game_env):
		center = game_env.getCurrentLocation()
		# you can scan only 10 tiles arround the robot so start at top right corner
		curr = (max(0, center[0] - 9), max(0, center[1] - 9))
		# clear enemies list since some enemies might not be a threat anymore
		self.enemies.clear()
		# go through the scope and store the map
		for i in range(curr[1], center[1] + 10):
			for j in range(curr[0], center[0] + 10):
				# check if current tile is valid
				temp = (j, i)
				if j < 0 or i < 0:
					continue
				# Check if duplicate
				if temp not in self.graph_origin:
					self.graph_origin[temp] = game_env.scanSpace(temp[0], temp[1])
					# add items
					if self.graph_origin[temp] == "Object":
						self.items.append(temp)
						self.num_items += 1
					# add threats for the first time (need to store the tile anyway)
					elif self.graph_origin[temp] == "Enemy":
						self.enemies.append(temp)
				# update an existing tile
				elif self.graph_origin[temp] != game_env.scanSpace(temp[0], temp[1]):
					self.graph_origin[temp] = game_env.scanSpace(temp[0], temp[1])
					# readd threats
					if (abs(temp[0] - center[0]) < 3 and abs(temp[1] - center[1]) < 3) and self.graph_origin[temp] == "Enemy":
						self.enemies.append(temp)

	# find the neighboring tiles in Gametype 3
	def online_neighbors(self, current):
		temp = []
		# look for all the 4 possibilities
		for node_next in ((current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1),
						  (current[0], current[1] - 1)):
			if (node_next[0], node_next[1]) in self.graph_origin and self.graph_origin[
				(node_next[0], node_next[1])] != "Wall":
				temp.append(node_next)
		return temp

	# A* using the map
	def online_astar(self, game_env, node, array):
		temp = None
		# find the closet tile to the goal "node"
		mini = None
		# clear the array to make space for a new path
		array.clear()
		start = game_env.getCurrentLocation()
		border = {(start[0], start[1]): 0}
		origin = {(start[0], start[1]): None}
		cost_so_far = {(start[0], start[1]): 0}
		while len(border):
			current = list(border.keys())[list(border.values()).index(min(border.values()))]
			border.pop(current)
			if current == node:
				temp = node
				break
			for node_next in self.online_neighbors(current):
				new_cost = cost_so_far[current] + 1
				if node_next not in cost_so_far or new_cost < cost_so_far[node_next]:
					cost_so_far[node_next] = new_cost
					priority = new_cost + self.heuristic(node, node_next)
					border[node_next] = priority
					origin[node_next] = current
					if mini is None or priority - new_cost <= mini[1]:
						mini = (node_next, priority - new_cost)
		# if the goal is unreachable then stop
		if node in self.graph_origin and node not in origin:
			if node == tuple(game_env.getGoal()):
				array.append((start[0] + 1,	start[1] + 1))
				return
		# if tile unreachable with current knowledge
		if temp is None:
			# if the robot is blocked then return
			if mini is None:
				return
			node = mini[0]
		# Store the path in the array
		while True:
			if origin[tuple(node)] is None:
				break
			array.append(tuple(node))
			node = origin[tuple(node)]
		return

	# When we do not need to explore yet
	def get_move_online(self, game_env):
		curr = tuple(game_env.getCurrentLocation())
		goal = tuple(game_env.getGoal())
		# if explore path still has moves left erase them
		self.explore_path.clear()
		# if there is a predetermined path and (the robot is not carrying an object and has a target
		# or it is carrying but not target or there are no objects left)
		if len(self.solution) and ((not game_env.robotCarrying() and self.curr_item is not None)
								   or (game_env.robotCarrying() and self.curr_item is None) or
								   (self.num_items == game_env.numberOfObjs()) and len(self.items) == 0):
			self.check_enemy(game_env, self.solution)
			return self.direction(self.solution.pop(), curr)
		# No item here going in
		if not game_env.robotCarrying():
			# on an object grab it
			if curr == self.curr_item and game_env.scanSpace(curr[0], curr[1]) == "Object":
				# Check if you should stay on the object to be invincible
				if self.check_enemy(game_env, self.solution):
					self.curr_item = None
					return "GRAB"
				return self.direction(self.solution.pop(), curr)
			# Move towards a new object
			else:
				# Available items go get em
				if len(self.items) > 0:
					self.curr_item = self.items.pop()
					self.online_astar(game_env, self.curr_item, self.solution)
					return self.get_move_online(game_env)
				else:
					# At the goal with no item
					if curr == goal:
						return "STOP"
					# not at goal no available item
					self.curr_item = None
					self.online_astar(game_env, goal, self.solution)
					return self.get_move_online(game_env)
		# Drop the item
		else:
			# At the goal drop the item
			if curr == goal:
				return "DROP"
			# Go to the goal
			else:
				self.online_astar(game_env, goal, self.solution)
				return self.get_move_online(game_env)

	# Updates a 7*7 tile to know if the robot has explored everything in it
	def update_tile(self, node):
		# Get the top left corner of the 7*7 tile
		x = node[1] * 7
		y = node[0] * 7
		temp = 0
		wall = 0
		# Check every node in that tile
		for i in range(y, y + 7):
			for j in range(x, x+7):
				if (i, j) in self.graph_origin:
					temp += 1
					if self.graph_origin[(i, j)] == "Wall":
						wall += 1
		# If it is filled with walls
		if wall == 49:
			# end of maze
			self.explore_tile[node] = 2
		# If the tile is fully explored
		elif temp == 49:
			# explored
			self.explore_tile[node] = 1
		# tile is partially or not explored
		else:
			self.explore_tile[node] = 0
		return self.explore_tile[node]

	# Update the map of explored 7*7 tiles and find new unexplored or partially explored tiles
	def update_array(self, game_env):
		# This adds the top left tile (or first tile)
		if (0, 0) not in self.explore_tile:
			temp = 0
			for i in range(7):
				for j in range(7):
					if (i, j) in self.graph_origin:
						temp += 1
			if temp == 49:
				# explored
				self.explore_tile[(0, 0)] = 1
			else:
				self.explore_tile[(0, 0)] = 0
		col = 0
		while True:
			temp = 0
			# Checks all tiles
			for i in range(math.ceil(game_env.getGoal()[0]/7)):
				if self.update_tile((col, i)):
					temp += 1
			# Checks for incomplete tiles in the current column
			if temp != math.ceil(game_env.getGoal()[0]/7):
				break
			col += 1
		return col

	# This gets the next node to explore to fill in the map
	def get_explore(self, game_env):
		col = self.update_array(game_env)
		i = 0
		while (col, i) in self.explore_tile:
			if self.explore_tile[(col, i)] == 0:
				break
			i += 1
		return (3 + col*7, 3 + i*7)

	# This handles the exploring part of the robot AI
	def explore(self, game_env):
		curr = tuple(game_env.getCurrentLocation())
		goal = tuple(game_env.getGoal())
		# If it has a path already then follow it
		if len(self.explore_path):
			# Check if it is safe to continue
			self.check_enemy(game_env, self.explore_path)
			return self.direction(self.explore_path.pop(), curr)
		# Finds the goal if it isn t discovered yet
		if goal not in self.graph_origin:
			self.online_astar(game_env, goal, self.explore_path)
			return self.explore(game_env)
		# Finds the node to go to to explore the map
		else:
			node = self.get_explore(game_env)
			self.online_astar(game_env, node, self.explore_path)
			return self.explore(game_env)

	# Check if it is safe to continue on the same path
	def check_enemy(self, game_env, array):
		number_of_enemies = len(self.enemies)
		# if no threats
		if number_of_enemies == 0:
			self.tries == 0
			return True
		curr = tuple(game_env.getCurrentLocation())
		# add all possible moves including wait
		my_moves = [curr]
		my_moves.extend(self.online_neighbors(curr))
		# Goes through all threats and removes unsafe moves
		for i in self.enemies:
			# Get all possible moves from the enemy
			possible_moves = self.online_neighbors(i)
			# If I am on a safe spot and in possible danger then just stay there
			if curr in possible_moves and game_env.scanSpace(curr[0], curr[1]) in ("Object", "Goal"):
				array.append(curr)
				return False
			if i in my_moves:
				my_moves.remove(i)
			# removes any remaining dangerous moves
			my_moves = [x for x in my_moves if x not in possible_moves]
		# if it is safe to continue on your path then continue
		try:
			if array[-1] in my_moves:
				self.tries == 0
				return True
		except IndexError:
			pass
		if self.tries < 10:
			if curr in my_moves:
				array.append(curr)
				self.tries += 1
				return False
		# On an object need to grab it
		if array == [] and self.curr_item is not None and game_env.scanSpace(curr[0], curr[1]):
			self.tries == 0
			return True
		# try to find another path
		else:
			new_path = []
			for i in self.enemies:
				self.graph_origin[i] = "Wall"
				temp = self.online_neighbors(i)
				for j in temp:
					if j in self.online_neighbors(curr):
						self.graph_origin[j] = "Wall"

			self.online_astar(game_env, array[0], new_path)
			# If the path works and has the same goal
			if new_path != [] and new_path[0] == array[0]:
				array.clear()
				array.extend(new_path)
				self.tries == 0
				return True
			# No other path try to stall and stay safe
			else:
				if curr in my_moves:
					array.append(curr)
					return False
				if len(my_moves) > 0:
					array.append(curr)
					array.append(my_moves[random.randrange(0, len(my_moves))])
					return False
				else:
					print("No safe choice Continuing forwards")
					return True

	# Makes all submethods work together
	def next_move3(self, game_env):
		# store maze scope
		self.store(game_env)
		# Check if there are no available items left and there are more in the env and this robot isn't trying to fetch one
		# or the goal is not discovered if this evaluates to true then explore
		if len(self.items) == 0 and self.num_items < game_env.numberOfObjs() \
				and self.curr_item is None or tuple(game_env.getGoal()) not in self.graph_origin:
			return self.explore(game_env)
		# other wise the robot can fetch an item or carry it to the goal
		return self.get_move_online(game_env)

	# Major debugging tool
	def print_state(self, game_env):
		view = ""
		symbols = {
			"U": "??",
			"Empty": "  ",
			"Wall": "██",
			"Goal": "GG",
			"Start": "SS",
			"Object": "££",
			"Enemy": "òó",
			"Robot": "◘◘",
			"Error": "**"
		}
		for i in range(-1, game_env.cols + 1):
			for j in range(-1, game_env.rows + 1):
				if (i, j) == tuple(game_env.getCurrentLocation()):
					view += "".join("◘◘")
				elif (i, j) in self.graph_origin:
					view += "".join(symbols[game_env.board.spaceEnv(i, j)])
				else:
					view += "".join("??")
			view += "\n"
		print(view)

	# Chooses the right method to call for the gametype
	def nextMove(self, game_env, gameType):
		game_type = {
			2: self.next_move2,
			3: self.next_move3,
		}

		# self.print_state(game_env)
		# return self.next_move2(game_env)
		return game_type.get(gameType)(game_env)
