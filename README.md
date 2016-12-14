# GoLEx

Game of Life Extended. Work in progress.

## Basic idea
- GoL made into a real game ("extended" to n strategies)
- a **strategy** decides how to pick the starting configuration of cells

> strategies share the same board

> strategies pick just one cell at a time and go in turns during the so-called **"buildup" round**

- if two strategies pick the same cell in the same turn, the latter one kills the other: each turn, the order of choice is shuffled, so no one should be in a huge advantage (not to mention that the chances of picking the same spot are small)

- if a strategy tries to replace an already existing cell (made in a previous turn), it gets penalized by having put its cell placed randomly

> the number of turns in the build-up round is determined by the board's dimensions

> strategies can adjust their selection based on the resulting board of the previous turn

> cells retain the information of their strategy

- the **"buildup" round** is defined by the number of cells a strategy can pick (their given turns)
- after the "buildup" round, GoL algorithm takes over and decides the game

> the algorithm here is extended in a way that a cell needs at least two **friendly** neighbor cells (made by the same strategy) to survive, however, more than 3 neighbors of **any** strategy kills it
> any empty spot (a 'dead' cell) is taken by the neighboring **majority** strategy (the strategy that has more (at least 3) of its cells in the dead cell area than the other)

- the **winning strategy** is the one whose cells survived in greater number after a defined amount of GoL rounds and/or when the other strategies die out

## How to work with it
- By definition, programmers are the real **players** here
- You can make your own strategies by extending the **Strategy class**
- Get inspired by the basic strategies defined in strategies.py
- Configure basic parameters in the init file and test from there 

More detailed documentation is coming soon.
