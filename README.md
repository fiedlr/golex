# GoLEx

Game of Life Extended. Work in progress.

## Basic idea
- GoL made into a real game ("extended" to n strategies)
- a **strategy** decides how to pick the starting configuration of cells

> strategies share the same board

> strategies pick just one cell at a time and go in turns during the so-called **"buildup" round**

> strategies can adjust their selection based on the resulting board of the previous turn

> cells retain the information of their strategy

- the **"buildup" round** is defined by the number of cells a strategy can pick (their given turns)
- after the "buildup" round, GoL algorithm takes over and decides the game
- the **winning strategy** is the one whose cells survived in greater number after a defined amount of GoL rounds and/or when the other strategies die out

## How to work with it
- By definition, programmers are the real **players** here
- You can make your own strategies by extending the **Strategy class**
- Get inspired by the basic strategies defined in strategies.py
- Configure basic parameters in the init file and test from there 

More detailed documentation is coming soon.
