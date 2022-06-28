# RubiksCubeSolver
---
## Solving Methods:
- Breadth-first Search
- Iterative Deepening Search 
- A* (heuristic based)

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
