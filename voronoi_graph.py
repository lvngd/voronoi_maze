import random
import math
from scipy.spatial import Voronoi
from helpers.slope import BoundingBoxIntercepts
from helpers.poisson import get_poisson_distribution

"""
-Generates a Voronoi diagram from random points using SciPy's Voronoi.
-Clips it to the 100x100 box for the maze.
-https://stackoverflow.com/a/57074133
	Explanation of why [(999,999), (-999,999), (999,-999), (-999,-999)] are added.

TODO - clean up code, probably find a better solution to clipping the Voronoi diagram
"""

class VoronoiGraph:
	def __init__(self,width,height):
		self.points = get_poisson_distribution(width-1,height-1)
		#adding these points - see stackoverflow link
		self.points.extend([(999,999), (-999,999), (999,-999), (-999,-999)])
		self.vor = Voronoi(self.points)
		self.corners = []
		#remove the -999,999 points after generating voronoi
		self.points = self.points[:-4]
		#cells/seed points and their neighbors
		self.cells = {}
		#cell seed point to a list of the walls making up the voronoi cell around it
		self.cell_walls = {}
		self.edge_side_points = []
		self.nodes,self.edges = self.get_voronoi_edges()
		self.updated_voronoi_edges = set()
		#graph_edges - cell/seed point neighbor edges
		#point pairs separating edges = edge that separates two voronoi cells
		self.graph_edges,self.point_pairs_separating_edges = self.edges_surrounding_input_points()
		self.get_neighbors()
		self.new_nodes = set()
		self.top_edges,self.bottom_edges,self.right_edges,self.left_edges = self.filter_voronoi_edges_in_bounds()

	def get_voronoi_edges(self):
		"""returns vertices and edges making up voronoi cells"""
		edges = set()
		nodes = set()
		for pair in self.vor.ridge_vertices: 
			if pair[0] >= 0 and pair[1] >= 1:
				first = self.vor.vertices[pair[0]] 
				second = self.vor.vertices[pair[1]] 
				edges.add((tuple(first),tuple(second)))
				nodes.add(tuple(first))
				nodes.add(tuple(second))
		return nodes, edges

	def check_if_in_range(self,edge):
		"""
		some voronoi points are way outside the bounding box, so calculate intercepts
		on whichever boundary they should be brought into.
		"""
		updated_edge = None
		left_side_out_of_bounds = False
		right_side_out_of_bounds = False
		p1 = edge[0]
		p1x = p1[0]
		p1y = p1[1]
		p2 = edge[1]
		p2x = p2[0]
		p2y = p2[1]
		box = BoundingBoxIntercepts(p1,p2)
		if p1x < 0:
			left_side_out_of_bounds = True
			updated_edge = 0
			left_boundary = box.left
			p1x = 0
			p1y = left_boundary
		if p1x > 100:
			left_side_out_of_bounds = True
			updated_edge = 0
			right_boundary = box.right
			p1x = 100
			p1y = right_boundary
		if p1y < 0:
			left_side_out_of_bounds = True
			updated_edge = 0
			bottom_boundary = box.bottom
			p1x = bottom_boundary
			p1y = 0
		if p1y > 100:
			left_side_out_of_bounds = True
			updated_edge = 0
			top_boundary = box.top
			p1x = box.top
			p1y = 100
		if p2x < 0:
			right_side_out_of_bounds = True
			updated_edge = 1
			left_boundary = box.left
			p2x = 0
			p2y = left_boundary
		if p2x > 100:
			right_side_out_of_bounds = True
			updated_edge = 1
			right_boundary = box.right
			p2x = 100
			p2y = right_boundary
		if p2y < 0:
			right_side_out_of_bounds = True
			updated_edge = 1
			bottom_boundary = box.bottom
			p2y = 0
			p2x = bottom_boundary
		if p2y > 100:
			right_side_out_of_bounds = True
			updated_edge = 1
			top_boundary = box.top
			p2x = box.top
			p2y = 100
		new_edge = ((p1x,p1y),(p2x,p2y))
		if left_side_out_of_bounds and right_side_out_of_bounds:
			#if points are completely out of bounds, don't keep the edge
			return
		return new_edge

	def check_for_side_edge(self,new_edges):
		"""adds in side edges to polygons, and fixes corners"""
		corner = False
		adjust = False
		#for sorting corner edges clockwise
		reference_vector = None
		side_edges = []
		x_100 = []
		y_100 = []
		x_zero = []
		y_zero = []
		for e in new_edges:
			p1 = e[0]
			p2 = e[1]
			if p1[0] == 0:
				x_zero.append(p1)
			elif p2[0] == 0:
				x_zero.append(p2)
			elif p1[0] == 100:
				x_100.append(p1)
			elif p2[0] == 100:
				x_100.append(p2)
			elif p1[1] == 0:
				y_zero.append(p1)
			elif p2[1] == 0:
				y_zero.append(p2)
			elif p1[1] == 100:
				y_100.append(p1)
			elif p2[1] == 100:
				y_100.append(p2)
		if len(x_100) == 2:
			e1 = (x_100[0],x_100[1])
			side_edges.append(e1)
		if len(y_100) == 2:
			e2 = (y_100[0],y_100[1])
			side_edges.append(e2)
		if len(x_zero) == 2:
			e3 = (x_zero[0],x_zero[1])
			side_edges.append(e3)
		if len(y_zero) == 2:
			e4 = (y_zero[0],y_zero[1])
			side_edges.append(e4)
		if len(x_zero) == 1 and len(y_zero) == 1:
			reference_vector = (0,0)
			corner = True
			e5 = (x_zero[0], (0,0))
			e6 = ((0,0), y_zero[0])
			side_edges.append(e5)
			side_edges.append(e6)
		if len(x_zero) == 1 and len(y_100) == 1:
			reference_vector = (0,100)
			corner = True
			e7 = (x_zero[0], (0,100))
			e8 = ((0,100), y_100[0])
			side_edges.append(e7)
			side_edges.append(e8)
		if len(y_100) == 1 and len(x_100) == 1:
			reference_vector = (100,100)
			corner = True
			e9 = (y_100[0], (100,100))
			e10 = ((100,100),x_100[0])
			side_edges.append(e9)
			side_edges.append(e10)
		if len(x_100) == 1 and len(y_zero) == 1:
			reference_vector = (100,0)
			corner = True
			e11 = (x_100[0],(100,0))
			e12 = ((100,0), y_zero[0])
			side_edges.append(e11)
			side_edges.append(e12)
		for edge in side_edges:
			new_edges.append(edge)
		if corner:
			new_edges = self.fix_corner_voronoi_cell(new_edges)
		return new_edges

	def fix_corner_voronoi_cell(self, edges):
		"""sort corner points by polar coordinates to fill in polygon correctly"""
		pp = []
		for e in edges:
			if e[0] not in pp:
				pp.append(e[0])
			if e[1] not in pp:
				pp.append(e[1])
		cent=(sum([p[0] for p in pp])/len(pp),sum([p[1] for p in pp])/len(pp))
		# sort by polar angle
		pp.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))
		surrounding_edges = []
		p1 = pp[0]
		i1 = pp[0]
		for point in pp[1:]:
			new_edge = (i1[0],i1[1]), (point[0],point[1])
			surrounding_edges.append(new_edge)
			i1 = point
		#connect last vertice with first vertice
		closing_edge = (i1[0],i1[1]), (p1[0],p1[1])
		surrounding_edges.append(closing_edge)
		return surrounding_edges

	def bounding_box_surrounding_edges(self,surrounding_edges):
		"""take surrounding edges of a voronoi seed point and clip all of them in sequence"""
		is_edge_cell = False
		new_edges = []
		for edge in surrounding_edges:
			prev_edge = edge
			updated = self.check_if_in_range(edge)
			if updated:
				updated_points = [updated[0][0],updated[0][1],updated[1][0],updated[1][1]]
				if 0 in updated_points:
					is_edge_cell = True
				elif 100 in updated_points:
					is_edge_cell = True
				new_edges.append(updated)
		new_edges = self.check_for_side_edge(new_edges)
		return new_edges,is_edge_cell

	def round_edge_numbers(self,edge,round_to):
		"""
		rounding the edge and reverse edge so that 
		they match up in the dictionary
		round_to = number of digits to round to
		"""
		edge_x = edge[0][0]
		edge_y = edge[0][1]
		edge2_x = edge[1][0]
		edge2_y = edge[1][1]
		first_edge = (round(edge_x,round_to),round(edge_y,round_to))
		second_edge = (round(edge2_x,round_to),round(edge2_y,round_to))
		rounded_edge = (first_edge,second_edge)
		reverse_rounded_edge = (second_edge,first_edge)
		return rounded_edge,reverse_rounded_edge

	def get_voronoi_edges_surrounding_point(self,i):
		"""takes point index and returns its surrounding cell edges from scipy voronoi"""
		reg = self.vor.point_region[i]
		region = self.vor.regions[reg]
		surrounding_edges = []
		p1 = self.vor.vertices[region[0]]
		i1 = self.vor.vertices[region[0]]
		for ind in region[1:]:
			current = self.vor.vertices[ind]
			new_edge = (i1[0],i1[1]), (current[0],current[1])
			surrounding_edges.append(new_edge)
			i1 = current
		#connect last vertice with first vertice
		closing_edge = (i1[0],i1[1]), (p1[0],p1[1])
		surrounding_edges.append(closing_edge)
		return surrounding_edges

	def edges_surrounding_input_points(self):
		"""
		populates cell_walls dictionary
		gets the edges that surround each input point and
		clips them to the bounding box (100x100)
		rounds the edge points because they weren't matching up after
		clipping
		"""
		#dictionary to hold voronoi side edge separating two cells
		point_pairs_to_edge_separating_them = {}
		graph_edges = set()
		edge_to_point = {}
		for i in range(len(self.points)):
			surrounding_edges = self.get_voronoi_edges_surrounding_point(i)
			#adjust edge if not in range
			surrounding_edges,side_point = self.bounding_box_surrounding_edges(surrounding_edges)
			#make a list of border points
			if side_point:
				if self.points[i] not in self.edge_side_points:
					self.edge_side_points.append(self.points[i])
			if self.points[i] not in self.cell_walls:
				self.cell_walls[self.points[i]] = surrounding_edges
			#find matching cells that share a separating edge - these are neighbors
			for edge in surrounding_edges:
				#rounding edge numbers so they match up
				rounded_edge,rounded_reverse_edge = self.round_edge_numbers(edge,2)
				if rounded_edge in edge_to_point:
					matching_point = edge_to_point[rounded_edge]
					path_edge = (self.points[i], matching_point)
					point_pairs_to_edge_separating_them[path_edge] = edge
					point_pairs_to_edge_separating_them[(matching_point,self.points[i])] = edge
					graph_edges.add(path_edge)
				elif rounded_reverse_edge in edge_to_point:
					matching_point = edge_to_point[rounded_reverse_edge]
					path_edge = (self.points[i], matching_point)
					point_pairs_to_edge_separating_them[path_edge] = edge
					point_pairs_to_edge_separating_them[(matching_point,self.points[i])] = edge
					graph_edges.add(path_edge)
				else:
					edge_to_point[rounded_edge] = self.points[i]
					edge_to_point[rounded_reverse_edge] = self.points[i]
		return graph_edges, point_pairs_to_edge_separating_them

	def get_neighbors(self):
		"""populates the graph/cells dictionary - seed points and their neighbors"""
		for edge in self.graph_edges:
			first = edge[0]
			second = edge[1]
			if first not in self.cells:
				self.cells[first] = [second]
			else:
				if second not in self.cells[first]:
					self.cells[first].append(second)
			if second not in self.cells:
				self.cells[second] = [first]
			else:
				if first not in self.cells[second]:
					self.cells[second].append(first)
		return

	def filter_voronoi_edges_in_bounds(self):
		"""filter out voronoi cell edges that are completely out of bounds"""
		top_edges = [] #y=100
		bottom_edges = [] #y=0
		right_edges = [] #x=0
		left_edges = [] #x=100
		for edge in self.edges:
			in_range = self.check_if_in_range(edge)
			if in_range:
				self.updated_voronoi_edges.add(in_range)
				p1 = in_range[0]
				p2 = in_range[1]
				self.new_nodes.add(p1)
				self.new_nodes.add(p2)
				e = [p1,p2]
				e.sort()
				if p1[0] == 0:
					right_edges.append(tuple(e))
				elif p2[0] == 0:
					right_edges.append(tuple(e))
				elif p1[0] == 100:
					left_edges.append(tuple(e))
				elif p2[0] == 100:
					left_edges.append(tuple(e))
				elif p1[1] == 0:
					bottom_edges.append(p1)
				elif p2[1] == 0:
					bottom_edges.append(p2)
				elif p1[1] == 100:
					top_edges.append(p1)
				elif p2[1] == 100:
					top_edges.append(p2)
		return top_edges,bottom_edges,right_edges,left_edges

	def draw_right_edges(self):
		"""add right edges to the Voronoi diagram plot"""
		right_edges = sorted(self.right_edges, key=lambda x:x[0][1])
		first = (0,0)
		self.new_nodes.add(first)
		for r in right_edges:
			p1 = first
			p2 = r[0]
			new_edge = (p1,p2)
			first = r[0]
			self.updated_voronoi_edges.add(new_edge)
		last = (0,100)
		self.updated_voronoi_edges.add((first,last))
		self.new_nodes.add(last)
		return

	def draw_left_edges(self):
		"""add left edges to the Voronoi diagram plot"""
		left_edges = sorted(self.left_edges, key=lambda x:x[1][1])
		first = (100,0)
		self.new_nodes.add(first)
		for l in left_edges:
			p1 = first
			p2 = l[1]
			new_edge = (p1,p2)
			first = l[1]
			self.updated_voronoi_edges.add(new_edge)
		last = (100,100)
		self.updated_voronoi_edges.add((first,last))
		self.new_nodes.add(last)
		return

	def draw_bottom_edges(self):
		"""add bottom edges to the Voronoi diagram plot"""
		bottom_edges = sorted(self.bottom_edges, key=lambda x:x[0])
		first = (0,0)
		self.new_nodes.add(first)
		for b in bottom_edges:
			new_edge = (first,b)
			first = b
			self.updated_voronoi_edges.add(new_edge)
		last = (100,0)
		self.new_nodes.add(last)
		last_edge = (first,last)
		self.updated_voronoi_edges.add(last_edge)
		return

	def draw_top_edges(self):
		"""add top edges to the Voronoi diagram plot"""
		top_edges = sorted(self.top_edges, key=lambda x:x[0])
		first = (0,100)
		self.new_nodes.add(first)
		for t in top_edges:
			new_edge = (first,t)
			first = t
			self.updated_voronoi_edges.add(new_edge)
		last = (100,100)
		self.new_nodes.add(last)
		last_edge = (first,last)
		self.updated_voronoi_edges.add(last_edge)
		return