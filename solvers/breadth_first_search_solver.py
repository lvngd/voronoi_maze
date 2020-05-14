from collections import deque

class MazeSolverBFS:
	def __init__(self,maze):
		self.maze = maze
		self.path = self.solve_maze_bfs()

	def solve_maze_bfs(self):
		"""returns breadth-first search path for matplotlib animation"""
		self.name = 'voronoi-bfs'
		visited = []
		queue = deque([self.maze.start])
		while queue:
			current = queue.pop()
			visited.append(current)
			if current == self.maze.exit:
				#found exit
				break
			neighbors = self.maze.graph[current]
			for neighbor in neighbors:
				edge = (current,neighbor)
				reverse_edge = (neighbor,current)
				if edge in self.maze.legal_maze_path_edges and neighbor not in visited:
					queue.appendleft(neighbor)
				elif reverse_edge in self.maze.legal_maze_path_edges and neighbor not in visited:
					queue.appendleft(neighbor)				
		return visited