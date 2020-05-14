import random
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from voronoi_maze import VoronoiMaze


class LoopingPillowWriter(PillowWriter):
	def finish(self):
		self._frames[0].save(
			self._outfile, save_all=True, append_images=self._frames[1:],
			duration=int(1000 / self.fps), loop=0)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=550)

class VoronoiMazePlot:
	"""optional pass in colors_dict of colors for plot"""
	def __init__(self, maze, colors_dict=None):
		self.maze = maze
		self.maze_line_thickness = 1
		if not colors_dict:
			self.background_color = "teal"
			self.maze_line_color = "white"
			self.neighbor_line_color = "orange"
			self.point_color = "orange"
			self.start_color = "orange"
			self.exit_color = "red"
			self.polygon_face_color = "yellow"
			self.polygon_edge_color = "none"
			self.polygon_backtracking_color = "purple"
			self.polygon_backtracking_edge_color = "none"
		else:
			self.set_colors(colors_dict)
		self.name = 'voronoi-maze'

		self.fig,self.ax = self.initialize_plot()
		self.draw_voronoi()
		self.draw_maze()
		
	def set_colors(self, colors_dict):
		print("setting colors")
		self.background_color = colors_dict.get("background_color")
		self.maze_line_color = colors_dict.get("maze_line_color")
		self.neighbor_line_color = colors_dict.get("neighbor_line_color")
		self.point_color = colors_dict.get("point_color")
		self.start_color = colors_dict.get("start_color")
		self.exit_color = colors_dict.get("exit_color")
		self.polygon_face_color = colors_dict.get("polygon_face_color")
		self.polygon_edge_color = colors_dict.get("polygon_edge_color")
		self.polygon_backtracking_color = colors_dict.get("polygon_backtracking_color")
		self.polygon_backtracking_edge_color = colors_dict.get("polygon_backtracking_edge_color")
		return

	def initialize_plot(self):
		"""set up matplotlib plot"""
		fig = plt.figure(figsize = (5,5))
		ax = self.reset_axis()
		return fig,ax

	def reset_axis(self):
		"""setup matplotlib axis or reset to redraw maze"""
		ax = plt.axes()
		ax.set_aspect("equal")
		ax.axes.get_yaxis().set_visible(False)
		ax.axes.get_xaxis().set_visible(False)
		plt.gca().set_axis_off()
		plt.margins(0.009,0.009)
		return ax

	def clear_maze(self):
		"""clears previous plot polygons for each new path solver"""
		[p.remove() for p in reversed(self.ax.patches)]
		self.draw_enter_exit()
		return

	def draw_seed_points(self,seed_thickness=0.5):
		px = [p[0] for p in self.maze.voronoi.points]
		py = [p[1] for p in self.maze.voronoi.points]
		self.ax.scatter(px,py,s=seed_thickness,color=self.point_color)
		return

	def draw_enter_exit(self):
		"""plot enter and exit cells on the graph"""
		start_polygon = Polygon(self.get_polygon_points(self.maze.start),True)
		exit_polygon = Polygon(self.get_polygon_points(self.maze.exit),True)
		start_polygon.set_facecolor(self.start_color)
		exit_polygon.set_facecolor(self.exit_color)
		exit_polygon.set_alpha(0.4)
		self.ax.add_patch(start_polygon)
		self.ax.add_patch(exit_polygon)
		return

	def draw_voronoi(self):
		"""draws the full voronoi diagram"""
		self.draw_seed_points(seed_thickness=5)
		for edge in self.maze.voronoi.updated_voronoi_edges:
			first = edge[0]
			second = edge[1]
			self.ax.plot([first[0],second[0]], [first[1],second[1]], color=self.maze_line_color,linewidth=self.maze_line_thickness)
		plt.savefig("visualizations/initial_voronoi_diagram.png", bbox_inches='tight', pad_inches=0.0)
		for edge in self.maze.voronoi.graph_edges:
			first = edge[0]
			second = edge[1]
			self.ax.plot([first[0],second[0]], [first[1],second[1]],color=self.neighbor_line_color,linewidth=self.maze_line_thickness)
		plt.savefig("visualizations/voronoi_neighbors.png", bbox_inches='tight', pad_inches=0.0)
		#clear axis
		plt.cla()
		return

	def draw_maze(self):
		self.ax = self.reset_axis()
		self.draw_seed_points()
		for edge in self.maze.voronoi.updated_voronoi_edges:
			first = edge[0]
			second = edge[1]
			if edge in self.maze.edges_to_remove:
				pass
			elif (second,first) in self.maze.edges_to_remove:
				pass
			else:
				self.ax.plot([first[0],second[0]], [first[1],second[1]], color=self.maze_line_color,linewidth=self.maze_line_thickness)
		patches = []
		self.draw_enter_exit()
		plt.savefig("visualizations/voronoi_maze_initial.png", bbox_inches='tight', pad_inches=0)
		return

	def get_polygon_points(self,point):
		"""gets points to create matplotlib Polygon object"""
		polygon_points = []
		for wall in self.maze.voronoi.cell_walls[point]:
			if wall[0] not in polygon_points:
				polygon_points.append(wall[0])
			if wall[1] not in polygon_points:
				polygon_points.append(wall[1])
		return polygon_points

	def animate(self):
		anim = animation.FuncAnimation(self.fig,self.animate_polygons,frames=len(self.path),interval=5,blit=True,repeat=False)
		anim.save('visualizations/voronoi_animation-{}.mp4'.format(self.name), writer=writer)
		return

	def animate_polygons(self,frame):
		point = self.path[frame]
		polygon = Polygon(self.get_polygon_points(point),True)
		if point not in [self.maze.start,self.maze.exit]:
			if point in self.path[:frame]:
				#backtracking
				polygon.set_facecolor(self.polygon_backtracking_color)
				polygon.set_edgecolor(self.polygon_backtracking_edge_color)
				self.ax.add_patch(polygon)
			else:
				polygon.set_facecolor(self.polygon_face_color)
				polygon.set_edgecolor(self.polygon_edge_color)
				self.ax.add_patch(polygon)
		if point == self.maze.exit:
			polygon.set_facecolor(self.exit_color)
			polygon.set_alpha(1)
			self.ax.add_patch(polygon)
		return []