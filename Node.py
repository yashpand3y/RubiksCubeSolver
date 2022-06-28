class CubeNode:
	def __init__(self, cur_cube):
		self.moves_applied = []
		self.children = []
		self.moves_to_create_children = []
		self.current_cube_state = cur_cube
		self.parent = None
		self.depth = 0
		self.heuristic = -1
