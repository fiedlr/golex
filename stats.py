""" golex v0.7 <github.com/fiedlr/golex> | (c) 2016 Adam Fiedler | <opensource.org/licenses/MIT> """

from main import Game
from strategies import *

# Winner container
winners = []

# Make 100 games
for i in range(100):
	game = Game([10, 20], 100, 0)
	strategies = [Ship(game), Castle(game)]
	# Opposing strategies
	game.add_strategy(strategies[0]).add_strategy(strategies[1])
	# Build
	game.build()
	# Run
	game.run()
	# Winner
	if game.get_winner() != None:
		winners.append(strategies.index(game.get_winner()))
	else:
		winners.append(-1)

print("Ship#1 wins:", winners.count(0), "Castle wins:", winners.count(1), "Draws:", winners.count(-1))
print("Ship chance of winning against castle: ", winners.count(0) / len(winners))