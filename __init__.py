""" <github.com/fiedlr/golex> | (c) 2016 Adam Fiedler | <opensource.org/licenses/MIT> """

from main import Game
from strategies import *

def run(dimensions, turns, terminal=1):
	""" Run a game with the chosen config - accessible through terminal """

	# Run the game
	game = Game(dimensions, turns, terminal) # debug flag = 1
	strategy1 = Ship(game)
	strategy2 = Ship(game, "~")

	# Opposing strategies
	game.add_strategy(strategy1).add_strategy(strategy2)

	# Choose the board
	print("Welcome to Game of Life Extended (codename golex) v.", game.VERSION)
	print("This game takes GoL to the next level by bringing more civilizations together and making them fight each other.\n")

	# Start line
	print("Initial configuration with the chosen strategies (", strategy1.SIGN, ",", strategy2.SIGN, "):")

	# Set up the initial configuration
	game.build()

	# Make user see what's happening
	if terminal:
		input("Press Enter to continue")

	print("\nProceeding with the simulation...")

	# Iterate through the GoL algorithm
	game.run()

	winner = game.get_winner()

	print("Resulting board:")

	game.print_state()

	print()

	# Show the winner
	print("After", turns, "turns, the winning strategy is '", winner, "'")

	# End line
	print()

	return winner

# Run the game with these parameters
run([10, 20], 100, 1)
