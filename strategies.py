""" golex v0.7 <github.com/fiedlr/golex> | (c) 2016 Adam Fiedler | <opensource.org/licenses/MIT> """

from main import Strategy
import random

class Lottery(Strategy):
	""" Random strategy """
	SIGN = "X"

class Mirror(Strategy):
	""" Mirroring opponent's moves """
	SIGN = "O"

	def __init__(self, game, custom_sign=""):
		super(Mirror, self).__init__(game, custom_sign)
		# Internal clock to fight off the randomized 1st chooser
		self.__turn = 0
		self.__offset = [0, random.randint(-game.get_config("dimensions")[1] / 4, -game.get_config("dimensions")[1] / 4)]

	def next_pick(self, turn):
		# Halt the first time
		if self.get_game().get_config('strategies') == 2:
			opponent = self.get_game().get_opponent_state(self)
		else:
			opponent = []
		pick = 0
		if turn > 1 and self.__turn < len(opponent):
			# Copy other's movements
			pos = opponent[self.__turn].get_position()
			pick = [pos[0] + self.__offset[0], pos[1] + self.__offset[1]]
			self.__turn += 1
		return pick

class Castle(Strategy):
	""" Super-conservative strategy, pick one edge and stay there forever """
	SIGN = "^"

	def __init__(self, game, custom_sign=""):
		super(Castle, self).__init__(game, custom_sign)
		# Pick a random initial position
		self.__edges = [[0, 0], [0, game.get_config("dimensions")[1] - 2], [game.get_config("dimensions")[0] - 2, 0], [game.get_config("dimensions")[0] - 2, game.get_config("dimensions")[1] - 2]]

	def next_pick(self, turn):
		""" Conservative, non-moving strategy """
		if turn < 16:
			pos = [self.__edges[(turn // 4)][0] + ((turn % 4) // 2), self.__edges[(turn // 4)][1] + ((turn + 2) % 2)]
		else:
			pos = 0
		return pos

class Beacon(Strategy):
	""" Pick a random spot and create oscillations """
	SIGN = "*"

	def __init__(self, game, custom_sign=""):
		super(Beacon, self).__init__(game, custom_sign)
		# Pick a random initial position
		random_pos = game.get_random_free_position()
		self.__initial_position = [abs(random_pos[0] - 4), abs(random_pos[0] - 4)]

	def next_pick(self, turn):
		""" Choose fixed points based on the turn and halt afterwards """
		if turn < 8:
			pos = [self.__initial_position[0] + (turn // 2), self.__initial_position[1]]
			picks = [1, 2, 1, 2, 3, 4, 3, 4]
			pick = [pos[0], pos[1] + picks[turn % 8]]
		else:
			pick = 0
		return pick

class Ship(Strategy):
	""" Move along the board and destroy enemies """
	SIGN = "#"

	def __init__(self, game, custom_sign=""):
		super(Ship, self).__init__(game, custom_sign)
		# Pick a random initial position
		self.__initial_position = game.get_random_free_position()
		self.__pattern = [[0, 0], [0, 1], [-2, 1], [0, 2], [-1, 2]]

	def next_pick(self, turn):
		# Halt the first time
		if turn % 5 == 0:
			self.__initial_position = self.get_game().get_random_free_position()
		
		pos = [self.__initial_position[0] + self.__pattern[turn % 5][0], self.__initial_position[1] + self.__pattern[turn % 5][1]]

		return pos