import random
from voronoi_graph import VoronoiGraph


"""
class for generating the Voronoi diagram maze with randomized depth first search,
and solving the maze.

	-depth-first search
	-breadth-first search
	-depth-first search backtracking
	-dijkstra

"""

class VoronoiMaze:
	def __init__(self, width=100,height=100):
		self.voronoi = VoronoiGraph(width,height)
		self.graph = self.voronoi.cells
		self.edges_to_remove, self.legal_maze_path_edges = self.generate_maze()
		self.voronoi.draw_right_edges()
		self.voronoi.draw_left_edges()
		self.voronoi.draw_bottom_edges()
		self.voronoi.draw_top_edges()
		self.start,self.exit = self.get_enter_exit_locations()

	def generate_maze(self):
		"""
		randomized depth first search, and returns edges to remove from the 
		voronoi diagram, along with legal edges to traverse when solving
		"""
		def randomized_dfs(current,visited,edges_to_remove, legal_edges):
			visited.append(current)
			neighbors = self.graph[current]
			random.shuffle(neighbors)
			for n in neighbors:
				if n not in visited:
					legal_edges[(current,n)] = True
					legal_edges[(n,current)] = True
					edges_to_remove.append(self.voronoi.point_pairs_separating_edges[(current,n)])
					randomized_dfs(n,visited,edges_to_remove,legal_edges)
		start = self.voronoi.points[random.randint(0,len(self.voronoi.points)-1)]
		edges_to_remove = []
		#edges that are legal to traverse when solving the maze
		legal_traversal_edges = {}
		randomized_dfs(start,[],edges_to_remove,legal_traversal_edges)
		return edges_to_remove,legal_traversal_edges

	def get_enter_exit_locations(self):
		"""get enter and exit locations from edge points"""
		#just using first and last point for now because random points were often too close
		#nums = random.sample(range(0,len(self.voronoi.edge_side_points)-1),2)
		start = self.voronoi.edge_side_points[0]
		exit = self.voronoi.edge_side_points[-1]
		return start,exit