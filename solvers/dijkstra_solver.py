import heapq


class NodeWeight:
	"""node class for dijkstra maze solver"""
	def __init__(self,x,y,weight=0):
		self.x = x
		self.y = y
		self.weight = weight

	def __eq__(self,other):
		return self.weight == other.weight

	def __lt__(self,other):
		return self.weight < other.weight

	def __str__(self):
		return "{},{}".format(self.x,self.y)


class MazeSolverDijkstra:
	def __init__(self,maze):
		self.maze = maze
		self.path = self.solve_maze_dijkstra()

	def get_weight(self,node):
		"""gets the minimum distance from that node to any of the exit points"""
		x1 = node[0]
		y1 = node[1]
		x2 = self.maze.exit[0]
		y2 = self.maze.exit[1]
		weight = abs(x1-x2) + abs(y1-y2)
		return weight

	def solve_maze_dijkstra(self):
		"""returns dijkstra path for matplotlib animation"""
		self.name = 'voronoi-dijkstra'
		all_seen = []
		seen = []
		start_node = NodeWeight(self.maze.start[0],self.maze.start[1],self.get_weight(self.maze.start))
		queue = [start_node]
		heapq.heapify(queue)
		while queue:
			current = heapq.heappop(queue)
			seen.append((current.x,current.y))
			if (current.x,current.y) == self.maze.exit:
				return seen
			neighbors = self.maze.graph[(current.x,current.y)]
			for n in neighbors:
				legal_edge = False
				if n not in seen and not any(nd.x == n[0] and nd.y == n[1] for nd in queue):
					edge = ((current.x,current.y), (n[0],n[1]))
					reverse_edge = ((n[0],n[1]), (current.x,current.y))
					if edge in self.maze.legal_maze_path_edges:
						legal_edge = True
					elif reverse_edge in self.maze.legal_maze_path_edges:
						legal_edge = True
					if legal_edge:
						new_node = NodeWeight(n[0],n[1],self.get_weight(n))
						heapq.heappush(queue,new_node)
		return seen