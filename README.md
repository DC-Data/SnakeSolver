# Snake Solver

This repo is under heavy development.

Snake Solver is an AI-played Snake game, looking for perfect solution in shortest steps. The GUI is implemented with PyGame. The algorithm is a mixed method of BFS, Hamiltonian path, A* searching and forward checking.

# Algorithms

* A* algorithm: 

Calculate gscore and heuristic distance, then add them up as tentative gscore. Comparing T-gscore of possible moves to find best move.

* Forward checking: 

1) Find shortest Path(Based on BFS) between head and apple.

2) After the snake eats apple, Whether it can find its tail. If yes, then return the path from 1); If no, continue.

3) Let the snake move to its tail along the longest path (Adding steps into the shortest path to make it as longest as possible).

* Mixed Strategy(Forward Checking&BFS): 

1) Find shortest Path between head and apple.

2) After the snake eats apple, Whether it can find its tail. If yes, then return the path from 1); If no, continue.

3) Let the snake move one step (Choose one direction). After this move, the snake should find its tail and is farest from apple then the other three directions.

# Future works

* Almighty move:

Automatically construct a path or combination of pathes which covers the whole area of the graph.

## References
1. Al Sweigart. (2012). Wormy. Making Games with Python & Pygame. Retrieved from https://github.com/asweigart/making-games-with-python-and-pygame/blob/master/wormy/wormy.py
2. Shu Kong, Joan Aguilar Mayans. (2014). Automated Snake Game Solvers via AI Search Algorithms. Retrieved from http://sites.uci.edu/joana1/files/2016/12/AutomatedSnakeGameSolvers.pdf 
3. Chuyangliu. Path solver. Retrieved from https://github.com/chuyangliu/Snake/blob/master/docs/algorithms.md
