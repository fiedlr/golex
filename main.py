""" golex <github.com/fiedlr/golex> | (c) 2016 Adam Fiedler | <opensource.org/licenses/MIT> """

import math
import random
import os
import time

class Game:
	""" The main class takes care of the game instance. """
	VERSION = "0.6"

	def __init__(self, dimensions, turns, debug=0):
		if isinstance(turns, int) and isinstance(dimensions, list):
			# State containers
			self.__state = []
			self.__strategies = []
			# Configuration
			if len(dimensions) == 2 and isinstance(dimensions[0], int) and isinstance(dimensions[1], int):
				self.__dimensions = dimensions
			else:
				self.__dimensions = [10, 10]
			self.__turns = turns
			self.__debug = debug
			# Fill up the state container
			self.__fill()

	def __fill(self):
		""" Fill the virtual board with 'dead cells' (Nones) """
		for row in range(self.__dimensions[0]):
			self.__state.append([])
			for col in range(self.__dimensions[1]):
				self.__state[row].append(None)

	def __apply(self, adds, deletes):
		""" Apply the changes to the state """
		# This turned out to be faster than using temporary copies
		if isinstance(adds, list) and isinstance(deletes, list):
			for cell in adds:
				pos = cell.get_position()
				orig_cell = 0
				if self.is_taken(pos):
					orig_cell = self.get_cell(pos)
				self.__state[pos[0]][pos[1]] = cell
				if orig_cell:
					orig_cell.die()
			for cell in deletes:
				pos = cell.get_position()
				self.__state[pos[0]][pos[1]] = None
				# Destroy the instance and remove from strategy's internal state
				cell.die()

	def add_strategy(self, strategy):
		""" Adds a new strategy to the list of players (can be of same type) """
		# Limit the number of strategies to 2 for now
		if isinstance(strategy, Strategy) and len(self.__strategies) < 2:
			self.__strategies.append(strategy)
		# Allow chaining
		return self

	def get_opponent_state(self, requestor):
		""" To prevent looping through the entire get_state """
		# So far only for two players
		return self.__strategies[abs(self.__strategies.index(requestor)-1)].get_cells()

	def get_state(self):
		""" Strategies can naturally adjust their next picks based on the state """
		return self.__state

	def print_state(self):
		""" Print out the current state of the board """
		for row in self.__state:
			output = "| "
			for cell in row:
				output += cell.get_strategy().get_sign() if isinstance(cell, Cell) else " "
				output += " | "
			print(output[:-1])

	def build(self):
		""" Build up the starting board based on strategies' picks """
		# Add strategies first and make sure this does not run twice
		if len(self.__strategies) and not self.__state.count(Cell):
			# Initial turns are limited by the number of max(rows,cols)
			for turn in range(max(self.__dimensions[0], self.__dimensions[1])):
				# Apply  containers
				adds = []
				# Shuffle the choosing ground to minimise "overwrite" advantage
				random.shuffle(self.__strategies)
				for strategy in self.__strategies:
					cell = strategy.create_cell(strategy.next_pick(turn))
					if cell:
						adds.append(cell)
				# apply changes after the turn (no one gets the overseer advantage)
				self.__apply(adds, [])
			# print initial position
			if self.__debug:
				self.print_state()

	def run(self):
		""" Run n turns of the game """
		# A bit brute scan of all the positions each turn
		# There could be a faster algorithm through checking only on the living cells, but no time for it
		if len(self.__strategies):
			for turn in range(self.__turns):
				# apply containers
				adds = []
				deletes = []
				for row in range(self.__dimensions[0]):
					for col in range(self.__dimensions[1]):
						pos = [row, col]
						cell = self.get_cell(pos)
						neighbors = self.get_neighbors(pos, 0) # 0 for 'as strategies'
						# Conway's Game of Life algorithm + 'friendly count'
						if cell and (neighbors.count(cell.get_strategy()) < 2 or len(neighbors) > 3):
							deletes.append(cell)
						elif not cell and len(neighbors) == 3:
							adds.append(self.get_majority(neighbors).create_cell(pos))
				# apply changes after the turn for a correct processing
				self.__apply(adds, deletes)
				if self.__debug:
					self.print_state()
					#print('\n' * (self.__dimensions[0] - 10)) # 'refresh'
					time.sleep(0.1)
					os.system('clear') # system 'refresh' if supported

	def is_position(self, pos):
		""" Determine if the argument is a valid position """
		return (isinstance(pos, list) and len(pos) == 2 
				and isinstance(pos[0], int) and isinstance(pos[1], int) 
				and pos[0] >= 0 and pos[0] < self.__dimensions[0] 
				and pos[1] >= 0 and pos[1] < self.__dimensions[1])

	def is_taken(self, pos):
		""" Determine whether the given position is taken """
		return self.get_cell(pos) != None

	def get_cell(self, pos):
		""" Get cell on the given position """
		if self.is_position(pos):
			return self.__state[pos[0]][pos[1]]
		else:
			# Return for validation purposes
			return 0

	def get_neighbors(self, pos, as_cells=1):
		""" Get neighbors of the given position """
		neighbors = []
		# Check adjacent positions
		for i in range(8):
			# Convert the angle to the needed index
			angle = (math.pi / 4) * i
			row = pos[0] + round(math.sin(angle))
			col = pos[1] + round(math.cos(angle))
			# Check if this position contains a cell
			neighbor = self.get_cell([row, col])
			if neighbor:
				if as_cells:
					neighbors.append(neighbor)
				else:
					neighbors.append(neighbor.get_strategy())
		return neighbors

	def get_majority(self, cells):
		""" Get the major strategy in the cells list """
		# The majority for GoL(=3 fields regen) is ensured only if there are 2 players
		# In general, I need to scan n+1<=8 cells when having n<8 strategies for a majority
		if len(cells) == 3 and len(self.__strategies) == 2:
			return self.__strategies[0] if cells.count(self.__strategies[0]) > cells.count(self.__strategies[1]) else self.__strategies[1]
		elif len(self.__strategies) == 1:
			return self.__strategies[0]

	def get_random_free_position(self):
		""" Get a random position that is not taken """
		rand_pos = [None, None]
		# Repeat the selection until the position is available
		while self.is_taken(rand_pos):
			rand_pos[0] = random.randint(0, self.__dimensions[0] - 1)
			rand_pos[1] = random.randint(0, self.__dimensions[1] - 1)
		return rand_pos

	def get_winner(self):
		""" Determine the winner of the game in the current turn """
		winner = None
		num = 1
		record = 0
		for strategy in self.__strategies:
			# A little naive approach, but I'm trusting the strategies for now
			result = len(strategy.get_cells())
			if result > record:
				record = result
				winner = type(strategy).__name__ + ' ' + strategy.get_sign() if self.__debug else strategy # if 2 strat. of same kind
			elif result == record:
				winner = None
			num+=1
		return winner

	def get_random_offset(self, pos, width, height):
		""" Return a rand offset given the position for strategies to move """
		return [random.randint(-pos[0] + width, self.__dimensions[0] - pos[0] - width), random.randint(-pos[1] + height, self.__dimensions[1] - pos[1] - height)]

	def get_config(self, index):
		""" Get the game config in a new instance, protecting private vars """
		configs = {'dimensions': self.__dimensions, 'turns': self.__turns, 'debug': self.__debug, 'strategies': len(self.__strategies)}
		return configs[index]

class Strategy:
	""" Defines how to set up the initial board, a 'player' """
	SIGN = None # should be exactly one char long

	def __init__(self, game, custom_sign=""):
		""" Initiate within the given game """
		if isinstance(game, Game):
			# Game container
			self.__game = game
			# State container
			self.__cells = []
			# Design symbol
			self.__sign = custom_sign if custom_sign != "" else self.SIGN

	def get_game(self):
		""" Return the game within which this instance operates """
		return self.__game

	def get_cells(self):
		""" Return a list of this strategy's cells """
		return self.__cells

	def get_sign(self):
		return self.__sign

	def create_cell(self, pos):
		""" Makes the strategy do a new pick and adds it to its cells """
		new_cell = None
		# Strategy has a choice to be idle
		if pos != 0:
			new_cell = Cell(self, pos)
			# Append the new cell to the list automatically
			self.__cells.append(new_cell)
		# Return for the game engine to add it in the grid
		return new_cell

	def remove_cell(self, cell):
		""" Remove the cell from the cell list """
		# To prevent the outside to mess with internal mechanisms
		if self.__game.get_cell(cell.get_position()) is not self:
			self.__cells.remove(cell)

	def next_pick(self, turn):
		""" Strategy's core. How to pick a position in a new turn? Replace this in heirs """
		# Default behavior is random
		return self.__game.get_random_free_position()

class Cell:
	""" The core of the game mechanism: strategies and adjacent positions """

	def __init__(self, strategy, initial_pos):
		""" Places itself on the grid before the first round """
		if isinstance(strategy, Strategy):
			# Position container
			self.__strategy = strategy
			self.__pos = []
			# Save the initial position chosen by the strategy unless taken
			if not strategy.get_game().is_taken(initial_pos):
				self.__pos.append(initial_pos[0])
				self.__pos.append(initial_pos[1])
			else:
				self.__pos = self.__strategy.get_game().get_random_free_position()

	def get_strategy(self):
		""" Return cell's strategy to which it belongs """
		return self.__strategy

	def get_position(self):
		""" Return cell's position in the format [row,col] """
		return self.__pos

	def get_neighbors(self):
		""" Get cell's neighbors """
		return self.__strategy.get_game().get_neighbors(self.__pos)

	def die(self):
		""" Destroying the cell """
		self.__strategy.remove_cell(self)
		# is there any way how to turn on the garbage collector?
