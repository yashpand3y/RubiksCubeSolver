import copy
import sys
import collections
import random
import time
from typing import Dict, List, Any, Union

from Node import CubeNode

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

INVERSE_MOVE_MAP = {
	"U": "U'",
	"U'": "U",
	"R": "R'",
	"R'": "R",
	"F": "F'",
	"F'": "F",
	"D": "D'",
	"D'": "D",
	"L": "L'",
	"L'": "L",
	"B": "B'",
	"B'": "B"
}

DEFAULT_COLOR_MAP = {
	"G": "B",
	"O": "R",
	"W": "Y",
	"B": "G",
	"R": "O",
	"Y": "W"
}

COMPLEMENTARY_MOVE_MAP = {
	"U": "D'",
	"U'": "D",
	"D'": "U",
	"D": "U'",
	"L": "R'",
	"L'": "R",
	"R": "L'",
	"R'": "L",
	"F": "B'",
	"F'": "B",
	"B": "F'",
	"B'": "F"
}

COMPLEMENTARY_MOVES = {
	"UD'", "D'U",  # rotate whole cube left
	"U'D", "UD'",  # rotate whole cube right
	"L'R", "RL'",  # rotate the whole cube forward
	"LR'", "R'L",  # rotate whole cube backwards
	"FB'", "B'F",  # rotate whole cube clockwise
	"F'B", "BF'",  # rotate whole cube counter-clockwise
}

# x -> front down left : front down right
# y -> front down left : back down left
# z -> front down left : front top left
cube_array = [
	[0, 1, 0] , [1, 1, 0]
	[0]
]

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


# noinspection PyBroadException
class Cube:

	def __init__(self, string="WWWW RRRR GGGG YYYY OOOO BBBB"):
		# normalize stickers relative to a fixed corner
		try:
			# Check if Cube string is formatted correctly
			if self.check_cube_string_format(string):
				# Full Cube -> Array of each quadrant from every face
				self.cube_string = string
				self.full_cube = list(string.replace(" ", ""))
				self.update_cube_faces(self.full_cube)
			else:
				print("Invalid Cube Format")
		except Exception as e:
			print("Invalid Cube Format. Exiting...")
			raise e

	def check_cube_string_format(self, string):
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

	def update_cube_faces(self, string_list):
		string = "".join(string_list)
		self.top = string[:4]
		self.right = string[4:8]
		self.front = string[8:12]
		self.bottom = string[12:16]
		self.left = string[16:20]
		self.back = string[20:24]
		self.faces = [self.top, self.right, self.front, self.bottom, self.left, self.back]
		self.cube_string = " ".join(self.faces)

	# normalise faces of the Cube
	def norm(self):
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

	def equals(self, cube):
		self.norm()
		cube.norm()
		if self.full_cube == cube.full_cube:
			return True
		else:
			return False

	def clone(self):
		return Cube(" ".join(self.faces))

	# apply a move to a state
	# copy of Cube state needs to be passed (NOT DIRECT REFERNCE TO OBJECT)
	def applyMove(self, move, cube_state):
		self.norm()
		for map_index in MOVES[move]:
			index = MOVES[move].index(map_index)
			self.full_cube[index] = cube_state[map_index]
		self.update_cube_faces(" ".join(self.full_cube[::4]))
		return

	# apply a string sequence of moves to a state
	def applyMovesStr(self, alg, cube_state_string=""):
		for move in alg.split(" "):
			if cube_state_string == "":
				self.applyMove(move, self.full_cube.copy())
			else:
				self.full_cube = cube_state_string.copy()
				self.applyMove(move, cube_state_string)
		self.update_cube_faces("".join(self.full_cube))
		return

	# check if state is solved
	def isSolved(self):
		self.norm()
		if self.full_cube == list("WWWWRRRRGGGGYYYYOOOOBBBB"):
			return True
		else:
			return False

	# print state of the Cube
	def print(self, string_list=""):
		if string_list == "":
			string_list = self.full_cube.copy()
		print()
		self.update_cube_faces(string_list)
		top_str = f"   {self.top[:2]}\n   {self.top[2:]}"
		mid_str = f"{self.left[:2]} {self.front[:2]} {self.right[:2]} {self.back[:2]}"
		mid_2_str = f"{self.left[2:]} {self.front[2:]} {self.right[2:]} {self.back[2:]}"
		bot_str = f"   {self.bottom[:2]}\n   {self.bottom[2:]}"
		print(f"{top_str}\n{mid_str}\n{mid_2_str}\n{bot_str}")

	def shuffle(self, n):
		move_list = list(MOVES.keys())
		# random_move_list = random.sample(move_list, n)
		random_move_list = []
		# Generating random moves
		for _ in range(n):
			random_move_list.append(random.choice(move_list))
		[print(move, end = " ") for move in random_move_list]
		self.applyMovesStr(" ".join(random_move_list))
		return

	def random(self, alg, n=3):  # Cube starts from default
		if not n:
			n = 3
		self.applyMovesStr(alg, "WWWWRRRRGGGGYYYYOOOOBBBB")
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

	def get_possible_moves_for_node(self, node):
		possible_moves = [move for move in MOVES.keys()]
		try:
			last_move = node.moves_applied[-1]

			# check for inverse
			last_move_inverse = INVERSE_MOVE_MAP[last_move]
			possible_moves.remove(last_move_inverse)

			# check for complement
			move_complement = COMPLEMENTARY_MOVE_MAP[last_move]
			possible_moves.remove(move_complement)
		except IndexError:
			# no last move
			pass

		# check for 3 same moves in a row
		try:
			last_two_moves = node.moves_applied[-2:]
			if last_two_moves[0] == last_two_moves[1]:
				possible_moves.remove(last_two_moves[0])
		except IndexError:
			# 2 moves haven't yet been applied
			pass
		return possible_moves

	def print_triple_column(self, node_list):
		mod_three = len(node_list) % 3
		node_chunk_list = [node_list[i:i + 3] for i in range(0, len(node_list), 3)]
		row_space = (" " * 13) + "\t\t"
		for triplet in node_chunk_list:
			mod_three = len(triplet) % 3
			triplet = list(map(lambda x: x.current_cube_state, triplet))
			if mod_three == 0:
				top_str = f"   {triplet[0].top[:2]}{row_space}{triplet[1].top[:2]}{row_space}{triplet[2].top[:2]}{row_space}\t\t\n" \
						  f"   {triplet[0].top[2:]}{row_space}{triplet[1].top[2:]}{row_space}{triplet[2].top[2:]}{row_space}\t\t"
				mid_1_str = f"{triplet[0].left[:2]} {triplet[0].front[:2]} {triplet[0].right[:2]} {triplet[0].back[:2]}\t\t\t " \
							f"{triplet[1].left[:2]} {triplet[1].front[:2]} {triplet[1].right[:2]} {triplet[1].back[:2]}\t\t " \
							f"{triplet[2].left[:2]} {triplet[2].front[:2]} {triplet[2].right[:2]} {triplet[2].back[:2]}"
				mid_2_str = f"{triplet[0].left[2:]} {triplet[0].front[2:]} {triplet[0].right[2:]} {triplet[0].back[2:]}\t\t\t " \
							f"{triplet[1].left[2:]} {triplet[1].front[2:]} {triplet[1].right[2:]} {triplet[1].back[2:]}\t\t " \
							f"{triplet[2].left[2:]} {triplet[2].front[2:]} {triplet[2].right[2:]} {triplet[2].back[2:]}"
				bot_str = f"   {triplet[0].bottom[:2]}{row_space}{triplet[1].bottom[:2]}{row_space}{triplet[2].bottom[:2]}{row_space}\t\t\n" \
						  f"   {triplet[0].bottom[2:]}{row_space}{triplet[1].bottom[2:]}{row_space}{triplet[2].bottom[2:]}{row_space}"
				print(f"{top_str}\n{mid_1_str}\n{mid_2_str}\n{bot_str}\n")
			# if last incomplete triplet if present
			elif mod_three == 2:
				top_str = f"   {triplet[0].top[:2]}{row_space}{triplet[1].top[:2]}{row_space}\t\t\n" \
						  f"   {triplet[0].top[2:]}{row_space}{triplet[1].top[2:]}{row_space}\t\t"
				mid_1_str = f"{triplet[0].left[:2]} {triplet[0].front[:2]} {triplet[0].right[:2]} {triplet[0].back[:2]}\t\t\t " \
							f"{triplet[1].left[:2]} {triplet[1].front[:2]} {triplet[1].right[:2]} {triplet[1].back[:2]}\t\t"
				mid_2_str = f"{triplet[0].left[2:]} {triplet[0].front[2:]} {triplet[0].right[2:]} {triplet[0].back[2:]}\t\t\t " \
							f"{triplet[1].left[2:]} {triplet[1].front[2:]} {triplet[1].right[2:]} {triplet[1].back[2:]}\t\t"
				bot_str = f"   {triplet[0].bottom[:2]}{row_space}{triplet[1].bottom[:2]}{row_space}\t\t\n" \
						  f"   {triplet[0].bottom[2:]}{row_space}{triplet[1].bottom[2:]}{row_space}\t\t"
				print(f"{top_str}\n{mid_1_str}\n{mid_2_str}\n{bot_str}\n")
			else:
				triplet[0].print()

	def bfs(self, moves):
		# shuffle cube using moves
		start_cube = Cube()
		start_cube.applyMovesStr(moves)
		start_node = CubeNode(start_cube.clone())
		closed = []
		num_of_nodes = 0
		cur_node = copy.copy(start_node)
		open_nodes = [cur_node]
		moves_to_solution = ""
		nodes_to_solution = []
		start = time.time()
		end = None
		while len(open_nodes) > 0:
			cur_node = open_nodes[0]
			if cur_node.current_cube_state.isSolved():
				# return path to cur_node
				moves_to_solution = cur_node.moves_applied.copy()
				# get all nodes from goal to source
				tmp_node = copy.copy(cur_node)
				while tmp_node.parent is not None:
					nodes_to_solution.append(copy.copy(tmp_node))
					tmp_node = tmp_node.parent
				end = time.time()
				break
			# Generate moves to apply to generate children
			possible_moves = self.get_possible_moves_for_node(cur_node)
			cur_node.moves_to_create_children = possible_moves.copy()
			# Apply possible moves to each child
			# add child reference to node
			# create a clone of the cur_cube_state and apply each move in possible_moves
			# apply move
			for move in possible_moves:
				cube_clone = cur_node.current_cube_state.clone()
				cube_clone.applyMovesStr(move)
				# Create the node and append to open nodes
				new_node = CubeNode(cube_clone)
				new_node.parent = cur_node
				new_node.moves_applied = copy.copy(cur_node.moves_applied)
				new_node.moves_applied.append(move)
				cur_node.children.append(new_node)
				open_nodes.append(new_node)
			closed.append(open_nodes.pop(0))  # pop from open queue
			num_of_nodes += 1
		# get all nodes in path to root
		print("Solution found!")
		print(" ".join(moves_to_solution))
		# print cube state in 3 line format
		cube_list = [start_node]
		list_of_solution_path_nodes = [node for node in nodes_to_solution]
		list_of_solution_path_nodes.reverse()
		cube_list.extend(list_of_solution_path_nodes)
		self.print_triple_column(cube_list)
		# print time taken and num_of_nodes
		print(f"Time taken: {end - start} seconds")
		print(f"Nodes Traversed: {num_of_nodes}")
		return

	# def ids(self, moves):
	# 	cur_depth = 0
	# 	limit_reached = False
	# 	start_cube = Cube()
	# 	start_cube.applyMovesStr(moves)
	# 	start_node = CubeNode(start_cube)
	# 	depth_limit = 0
	# 	closed = []
	# 	cur_node = copy.copy(start_node)
	# 	open_nodes = [cur_node]
	# 	end = None
	# 	start = time.time()
	# 	while not limit_reached:
	# 		# dfs from source
	# 		path, limit_reached = self.dfs(open_nodes.pop(0), 0, depth_limit)
	# 		if path is not None:
	# 			end = time.time()
	# 			# output cubes here and time data
	# 			return
	# 		else:
	# 			depth_limit += 1
	#
	# 	# false case
	# 	return False
	#
	# def dfs(self, source_node, cur_depth, depth_limit):
	# 	path = None
	# 	reached_limit = False
	# 	cur_node = copy.copy(source_node)
	# 	if cur_node.current_cube_state.isSolved():
	# 		found = True
	# 		path = []
	# 		moves_to_solution = cur_node.moves_applied.copy()
	# 		# get all nodes from goal to source
	# 		tmp_node = copy.copy(cur_node)
	# 		while tmp_node.parent is not None:
	# 			path.append(copy.copy(tmp_node))
	# 			tmp_node = tmp_node.parent
	# 		end = time.time()
	# 		# print(f"Number of nodes explored at depth {depth_limit} = {nodes_visited_at_depth[depth_limit]}\n"
	# 		print(f"Solution found!")
	#
	# 	if cur_depth >= depth_limit:
	# 		if len(cur_node.children) > 0:
	# 			path = None
	# 			reached_limit = False
	# 			return path, reached_limit
	# 		else:
	# 			path = None
	# 			reached_limit = True
	# 			return path, reached_limit
	# 	reached_limit = True
	# 	for child in cur_node.children:
	# 		path, reached_limit_res = self.dfs(child, cur_depth + 1, depth_limit)
	# 		if path is not None:
	# 			return path, True
	# 		reached_limit = reached_limit and reached_limit_res
	#
	# 	return None, reached_limit

	def ids(self, moves):
		# shuffle cube using moves
		start_cube = Cube()
		start_cube.applyMovesStr(moves)
		start_node = CubeNode(start_cube)
		depth_limit = 0
		start = time.time()
		end = None
		cur_node = copy.copy(start_node)
		moves_to_solution = ""
		nodes_to_solution = []
		found_solution = False
		start_node_reference = cur_node
		layer_dict: dict[int, list[CubeNode]] = {}

		while True:
			if found_solution:
				# get all nodes in path to root
				print("Solution found! :- ")
				print(" ".join(moves_to_solution))
				# for key in nodes_visited_at_depth:
				# 	print(f"At depth {key}, nodes visited: {nodes_visited_at_depth[key]}")
				# implies change node counting method
				print()  # newline
				# print cube state in 3 line format
				for layer_num in layer_dict:
					print(f"Depth: {layer_num} d: {len(layer_dict[layer_num])}")
				cube_list = [start_node]
				list_of_solution_path_nodes = [node for node in nodes_to_solution]
				list_of_solution_path_nodes.reverse()
				cube_list.extend(list_of_solution_path_nodes)
				self.print_triple_column(cube_list)
				# print time taken and num_of_nodes
				print(f"Time taken: {end - start} seconds")
				# print(f"Nodes Traversed: {sum(nodes_visited_at_depth.values())}")
				# nodes_visited_at_depth[depth_limit] += num_of_nodes
				break
			open_nodes = [copy.copy(start_node_reference)]
			closed = []
			num_of_nodes_explored = 0
			new_layer = []
			# run dfs with current depth
			while len(open_nodes) > 0:  # Go through all
				# open_nodes should contain a list of nodes to go through in current dfs
				# dfs: generate nodes up till given depth
				# check each node at a given depth
				cur_node = open_nodes[0]
				# if reached bottom
				if cur_node.depth == depth_limit and len(closed) > 0:
					# pop all the children because each child.dept > depth_limit
					for _ in closed[-1].children:
						closed.append(open_nodes.pop(0))
						if closed[-1] not in new_layer:
							new_layer.append(closed[-1])
					continue
				if cur_node.current_cube_state.isSolved():
					found_solution = True
					# return path to cur_node
					moves_to_solution = cur_node.moves_applied.copy()
					# get all nodes from goal to source
					tmp_node = copy.copy(cur_node)
					while tmp_node.parent is not None:
						nodes_to_solution.append(copy.copy(tmp_node))
						tmp_node = tmp_node.parent
					end = time.time()
					# print(f"Number of nodes explored at depth {depth_limit} = {nodes_visited_at_depth[depth_limit]}\n"
					print(f"Solution found!")
					break
				# Generate moves to apply to generate children
				if not cur_node.children:
					# Indicates first time entering node
					possible_moves = self.get_possible_moves_for_node(cur_node)
					cur_node.moves_to_create_children = possible_moves
					possible_moves.reverse()
					if cur_node.depth == depth_limit:
						# if cur node already in layer
						if cur_node not in new_layer:
							new_layer.append(cur_node)
					# Apply possible moves to each child
					for move in possible_moves:
						cube_clone = cur_node.current_cube_state.clone()
						cube_clone.applyMovesStr(move)
						# Create the node and append to open nodes
						new_node = CubeNode(cube_clone)
						new_node.parent = cur_node
						new_node.moves_applied = copy.copy(cur_node.moves_applied)
						new_node.moves_applied.append(move)
						new_node.depth = cur_node.depth + 1
						cur_node.children.append(new_node)
						if new_node.depth <= depth_limit:
							open_nodes.insert(1, new_node)
				else:
					for child in cur_node.children:
						open_nodes.insert(1, child)
						if child.depth == depth_limit:
							new_layer.append(child)
				# if I pop open_nodes[0], run time is decreased because not spending time looking at nodes already
				# checked
				num_of_nodes_explored += 1
				closed.append(open_nodes.pop(0))
			try:
				layer_dict[depth_limit].append(new_layer)
			except Exception as _:
				layer_dict.update({depth_limit: new_layer})
			depth_limit += 1
		return

	def get_node_heuristic(self, node):
		# Heuristic is based on how many colors align on the face of each cube
		target_cube = Cube()
		cur_cube = node.current_cube_state.clone()
		cur_cube.norm()
		score = 24
		for target_face, current_cube_face in zip(target_cube.faces, cur_cube.faces):
			for target_color, current_cube_color in zip(target_face, current_cube_face):
				if target_color != current_cube_color:
					score -= 1
		return score

	def find_highest_heuristic_in_list(self, open_nodes):
		open_nodes_depth = list(map(lambda x: x.heuristic, copy.copy(open_nodes)))
		return open_nodes_depth.index(max(open_nodes_depth))

	def remove_with_key(self, index, d):
		r = d[index].pop(0)
		if not d[index]:
			del d[index]
		return r

	def astar(self, moves):
		start_cube = Cube()
		start_cube.applyMovesStr(moves)
		start_node = CubeNode(start_cube.clone())
		closed = []
		num_of_nodes = 0
		cur_node = copy.copy(start_node)
		open_nodes = [cur_node]
		moves_to_solution = ""
		nodes_to_solution = []
		start = time.time()
		end = None
		highest_heuristic_dict = {-1: [cur_node]}
		while len(open_nodes) > 0:
			max_heuristic = max(highest_heuristic_dict.keys())
			# cur_node = open_nodes[0]
			cur_node = highest_heuristic_dict[max_heuristic][0]
			if cur_node.current_cube_state.isSolved():
				# return path to cur_node
				moves_to_solution = cur_node.moves_applied.copy()
				# get all nodes from goal to source
				tmp_node = copy.copy(cur_node)
				while tmp_node.parent is not None:
					nodes_to_solution.append(copy.copy(tmp_node))
					tmp_node = tmp_node.parent
				end = time.time()
				break
			# Generate moves to apply to generate children
			possible_moves = self.get_possible_moves_for_node(cur_node)
			cur_node.moves_to_create_children = possible_moves.copy()
			# Apply possible moves to each child
			# add child reference to node
			# create a clone of the cur_cube_state and apply each move in possible_moves
			# apply move
			for move in possible_moves:
				cube_clone = cur_node.current_cube_state.clone()
				cube_clone.applyMovesStr(move)
				# Create the node and append to open nodes
				new_node = CubeNode(cube_clone)
				new_node.parent = cur_node
				new_node.moves_applied = copy.copy(cur_node.moves_applied)
				new_node.moves_applied.append(move)
				new_node.heuristic = new_node.depth + self.get_node_heuristic(new_node)
				cur_node.children.append(new_node)
				try:
					highest_heuristic_dict[new_node.heuristic].append(new_node)
				except KeyError:
					highest_heuristic_dict.update({new_node.heuristic: [new_node]})
				open_nodes.append(new_node)
			closed.append(self.remove_with_key(max_heuristic, highest_heuristic_dict))  # pop from open queue
			open_nodes.pop(open_nodes.index(cur_node))
			num_of_nodes += 1
		# get all nodes in path to root
		print("Solution found!")
		print(" ".join(moves_to_solution))
		# print cube state in 3 line format
		cube_list = [start_node]
		list_of_solution_path_nodes = [node for node in nodes_to_solution]
		list_of_solution_path_nodes.reverse()
		cube_list.extend(list_of_solution_path_nodes)
		self.print_triple_column(cube_list)
		# print time taken and num_of_nodes
		print(f"Time taken: {end - start} seconds")
		print(f"Nodes Traversed: {num_of_nodes}")
		return


if __name__ == '__main__':
	args = sys.argv
	argc = len(args)
	command = args[1]
	print(f"Command is: {command}")
	if argc == 2:  # command itself
		if command == "print":
			my_cube = Cube()
			my_cube.print()
	elif argc == 3:  # command w 1 arg
		augments = args[2:]
		if command == "print":
			my_cube = Cube(augments[0])
			my_cube.print()
		elif command == "goal":
			my_cube = Cube(augments[0])
			print(my_cube.isSolved())
		elif command == "norm":
			my_cube = Cube(augments[0])
			my_cube.norm()
			my_cube.print()
		elif command == "shuffle":
			my_cube = Cube()
			my_cube.shuffle(int(augments[0]))
			my_cube.print()
		elif command == "random":
			my_cube = Cube()
			my_cube.random(augments[0])
			my_cube.print()
		elif command == "bfs":
			my_cube = Cube()
			my_cube.bfs(augments[0])
		elif command == "ids":
			my_cube = Cube()
			my_cube.ids(augments[0])
		elif command == "astar":
			my_cube = Cube()
			my_cube.astar(augments[0])
	elif argc == 4:  # command w 3 args
		augments = args[2:]
		if command == "applyMovesStr":
			my_cube = Cube(augments[1])
			my_cube.applyMovesStr(augments[0])
			my_cube.print()
	else:
		print("Invalid Command (command not recognized)")

