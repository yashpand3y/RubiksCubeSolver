# RubiksCubeSolver
---
> This is only for a 2x2 cube
## Solving Methods:
- Breadth-first Search
- Iterative Deepening Search 
- A* (heuristic based)
---
Variables: 
- `cube_str`: 24 character string representing an entire cube
- `n`: Integer representing iteration count in different contexts
- `moves`: String of moves to apply on Rubiks Cube with ` ` as separator
---
The program uses terminal parametric inputs to tackle and do different functions.
- `print`: Prints, to the terminal, every side of a solved Rubiks Cube formatted as a flattened cube
- `print (str cube_str)`: Prints, to the terminal, every side of `cube_str` as a Rubiks Cube formatted as a flattened cube
- `goal (str cube_str)`: Returns **True** or **False** based on whether cube is solved or not
- `norm (str cube_str)`: Normalizes the cube using a hash map between corresponding colors using `DEFAULT_COLOR_MAP`
- `shuffle (int n)`: Applies a set of moves randomly on the cube
- `random (str moves, int n)`: Applies `moves` on a solved cube and applies `n` random moves to try and solve the cube.
- `bfs (str moves)`:  Applies `moves` on a solved cube and attempt to solve it using BFS algorithm.
- `ids (str moves)`: Applies `moves` on a solved cube and attempt to solve it using IDS algorithm
- `astar (str moves)`: Applies `moves` on a solved cube and attemmpts to solve it using A*. Heuristic is based on number of quadrants with the correct corresponding color.
- `applyMoveStr (str moves, str cube_str)`: Applies `moves` on given cube of cube state `cube_str`
---
Most of the code runs off an array of characters representing the colors on each face using the number system identified in the assignment document. 
This made cloning very easy for it’d be as simple as self.full_cube.copy().

I used python’s random standard library to generate a list of random moves to use in shuffle and random. I made sure that repetition is allowed.
The cube class has a list of faces (character arrays) which I use to check if cube is solved and when printing cube.

I created a map which holds each color and their opposites.
To check if the cube has returned to ground state, I compare the character array with what I expect a normalized character array to be.

If applyMovesStr is given a state to work from, it overwrites present cube’s state.

I tested this code locally using immediate test cases within the terminal itself.

The code itself is commented enough for understanding.

Because of system hardware limitations, I wasn't able to test with moves over 3. But for several combinations of moves, I wasn't able to test.

==The heuristic used for AStar was counting how many quadrants on each face has the correct color==
