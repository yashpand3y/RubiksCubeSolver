import random
import sys
import collections
import random

# different moves
# https://ruwix.com/online-puzzle-simulators/2x2x2-pocket-cube-simulator.php

MOVES = {
	"U": [2, 0, 3, 1, 20, 21, 6, 7, 4, 5, 10, 11, 12, 13, 14, 15, 8, 9, 18, 19, 16, 17, 22, 23],
	"U'": [1, 3, 0, 2, 8, 9, 6, 7, 16, 17, 10, 11, 12, 13, 14, 15, 20, 21, 18, 19, 4, 5, 22, 23],
	"R": [0, 9, 2, 11, 6, 4, 7, 5, 8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19, 3, 21, 1, 23],
	"R'": [0, 22, 2, 20, 5, 7, 4, 6, 8, 1, 10, 3, 12, 9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23],
	"F": [0, 1, 19, 17, 2, 5, 3, 7, 10, 8, 11, 9, 6, 4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23],
	"F'": [0, 1, 4, 6, 13, 5, 12, 7, 9, 11, 8, 10, 17, 19, 14, 15, 16, 3, 18, 2, 20, 21, 22, 23],
	"D": [0, 1, 2, 3, 4, 5, 10, 11, 8, 9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21, 6, 7],
	"D'": [0, 1, 2, 3, 4, 5, 22, 23, 8, 9, 6, 7, 13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19],
	"L": [23, 1, 21, 3, 4, 5, 6, 7, 0, 9, 2, 11, 8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12],
	"L'": [8, 1, 10, 3, 4, 5, 6, 7, 12, 9, 14, 11, 23, 13, 21, 15, 17, 19, 16, 18, 20, 2, 22, 0],
	"B": [5, 7, 2, 3, 4, 15, 6, 14, 8, 9, 10, 11, 12, 13, 16, 18, 1, 17, 0, 19, 22, 20, 23, 21],
	"B'": [18, 16, 2, 3, 4, 0, 6, 1, 8, 9, 10, 11, 12, 13, 7, 5, 14, 17, 15, 19, 21, 23, 20, 22],
}

DEFAULT_COLOR_MAP = {
	"G": "B",
	"O": "R",
	"W": "Y",
	"B": "G",
	"R": "O",
	"Y": "W"
}

'''
sticker indices:

      0  1
      2  3
16 17  8  9  4  5  20 21
18 19 10 11  6  7  22 23
      12 13
      14 15
10 (Green) -> 23 (Blue)
12 (Yellow) -> 2 (White)
19 (Orange) -> 6 (Red)
face colors:

    0
  4 2 1 5
    3

moves:
[ U , U', R , R', F , F', D , D', L , L', B , B']
'''


class cube:
	def __init__( self, string="WWWW RRRR GGGG YYYY OOOO BBBB" ):
		# normalize stickers relative to a fixed corner
		try:
			# Check if cube string is formatted correctly
			if self.check_cube_string_format(string):
				# Full Cube -> Array of each quadrant from every face
				self.full_cube = list(string.replace(" ", ""))
				self.update_cube_faces(self.full_cube)
			else:
				print("Invalid Cube Format")
		except Exception as e:
			print("Invalid Cube Format. Exiting...")
			raise (e)

	def check_cube_string_format( self, string ):
		# Check if there are 6 unique colors, 6 faces, and
		pass_check = True
		counter = collections.Counter(string.replace(" ", ""))
		# Check if each color has 4 instances
		for color in counter:
			if counter[color] != 4:
				print("Invalid Cube Formatting.")
				pass_check = False
		if len(counter) != 6:
			pass_check = False
		return pass_check

	def update_cube_faces( self, string_list ):
		string = "".join(string_list)
		self.top = string[:4]
		self.right = string[4:8]
		self.front = string[8:12]
		self.bottom = string[12:16]
		self.left = string[16:20]
		self.back = string[20:24]
		self.faces = [self.top, self.right, self.front, self.bottom, self.left, self.back]

	# normalise faces of the cube
	def norm( self ):
		# 10 -> Green, 12 -> Yellow, 19 -> Orange
		color_10, color_12, color_19 = self.full_cube[10], self.full_cube[12], self.full_cube[19]
		color_map = {
			color_10: "G",
			color_12: "Y",
			color_19: "O",
			DEFAULT_COLOR_MAP[color_10]: "B",
			DEFAULT_COLOR_MAP[color_12]: "W",
			DEFAULT_COLOR_MAP[color_19]: "R"
		}
		self.full_cube = list(map(color_map.get, self.full_cube))
		return

	def equals( self, cube ):
		self.norm()
		cube.norm()
		if self.full_cube == cube.full_cube:
			return True
		else:
			return False

	def clone( self ):
		return self.full_cube.copy()

	# apply a move to a state
	# copy of cube state needs to be passed (NOT DIRECT REFERNCE TO OBJECT)
	def applyMove( self, move, cube_state ):
		self.norm()
		for map_index in MOVES[move]:
			index = MOVES[move].index(map_index)
			self.full_cube[index] = cube_state[map_index]
		self.update_cube_faces("".join(self.full_cube))
		return

	# apply a string sequence of moves to a state
	def applyMovesStr( self, alg, cube_state_string="" ):
		for move in alg.split(" "):
			if cube_state_string == "":
				self.applyMove(move, self.full_cube.copy())
			else:
				self.full_cube = cube_state_string.copy()
				self.applyMove(move, cube_state_string)
		return

	# check if state is solved
	def isSolved( self ):
		self.norm()
		if self.full_cube == list("WWWWRRRRGGGGYYYYOOOOBBBB"):
			return True
		else:
			return False

	# print state of the cube
	def print( self, string_list="" ):
		if string_list == "":
			string_list = self.full_cube.copy()
		print()
		self.update_cube_faces(string_list)
		top_str = f"   {self.top[:2]}\n   {self.top[2:]}"
		mid_str = f"{self.left[:2]} {self.front[:2]} {self.right[:2]} {self.back[:2]}"
		mid_2_str = f"{self.left[2:]} {self.front[2:]} {self.right[2:]} {self.back[2:]}"
		bot_str = f"   {self.bottom[:2]}\n   {self.bottom[2:]}"
		print(f"{top_str}\n{mid_str}\n{mid_2_str}\n{bot_str}")

	def shuffle( self, n ):
		move_list = list(MOVES.keys())
		# random_move_list = random.sample(move_list, n)
		random_move_list = []
		# Generating random moves
		for _ in range(n):
			random_move_list.append(random.choice(move_list))
		[print(move, end = " ") for move in random_move_list]
		self.applyMovesStr(" ".join(random_move_list))
		return

	def random( self, alg, n=3 ):  # Cube starts from default
		if not n:
			n = 3
		self.applyMovesStr(alg, list("WWWWRRRRGGGGYYYYOOOOBBBB"))
		moves_used = []
		move_list = list(MOVES.keys())
		random_move_list = []
		# Generating random moves
		for _ in range(n):
			random_move_list.append(random.choice(move_list))
		print(f"List of random moves to pick and execute from: {random_move_list}")
		for move in random_move_list:
			self.applyMove(move, self.full_cube.copy())
			self.norm()
			if self.isSolved():
				print("Success!")
				break
			else:
				print("Failure")
				moves_used.append(move)


if __name__ == '__main__':
	args = sys.argv
	argc = len(args)
	command = args[1]
	print(f"Command is: {command}")
	if argc == 2:  # command itself
		if command == "print":
			my_cube = cube()
			my_cube.print()
	elif argc == 3:  # command w 1 arg
		augments = args[2:]
		if command == "print":
			my_cube = cube(augments[0])
			my_cube.print()
		elif command == "goal":
			my_cube = cube(augments[0])
			print(my_cube.isSolved())
		elif command == "norm":
			my_cube = cube(augments[0])
			my_cube.norm()
			my_cube.print()
		elif command == "shuffle":
			my_cube = cube()
			my_cube.shuffle(int(augments[0]))
			my_cube.print()
		elif command == "random":
			my_cube = cube()
			my_cube.random(augments[0])
			my_cube.print()
	elif argc == 4:  # command w 3 args
		augments = args[2:]
		if command == "applyMovesStr":
			my_cube = cube(augments[1])
			my_cube.applyMovesStr(augments[0])
			my_cube.print()
	else:
		print("Invalid Command (command not recognized)")
