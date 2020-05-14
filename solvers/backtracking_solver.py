import random

class MazeSolverBacktracking:
	def __init__(self, maze):
		self.maze = maze
		self.path = self.solve_maze_backtracking()

	def get_legal_neighbors(self, current,path):
		"""get neighbors that can be traversed to in the maze"""
		neighbors = []
		for n in self.maze.graph[(current)]:
			if n not in path:
				edge = (current,n)
				reverse_edge = (n,current)
				if edge in self.maze.legal_maze_path_edges:
					neighbors.append(n)
				elif reverse_edge in self.maze.legal_maze_path_edges:
					neighbors_append(n)
		return neighbors

	def solve_maze_backtracking(self):
		"""returns sbacktracking depth-first search path for matplotlib animation"""
		self.name = 'voronoi-backtracking'
		current = self.maze.start
		path = []
		seen = []
		while current != self.maze.exit:
			neighbors = self.get_legal_neighbors(current,path)
			if len(neighbors) > 0:
				seen.append(current)
				path.append(current)
				random_neighbor = neighbors[random.randint(0,len(neighbors)-1)]
				current = random_neighbor
			elif len(seen) > 0:
				path.append(current)
				current = seen.pop()
		path.append(current)
		return path