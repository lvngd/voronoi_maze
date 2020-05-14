from voronoi_maze import VoronoiMaze
from voronoi_maze_plots import VoronoiMazePlot
from solvers.depth_first_search_solver import MazeSolverDFS
from solvers.breadth_first_search_solver import MazeSolverBFS
from solvers.dijkstra_solver import MazeSolverDijkstra
from solvers.backtracking_solver import MazeSolverBacktracking


"""
Class to generate Voronoi diagram maze and run solvers.

1.  Depth-first search solver
2.  Breadth-first search solver
3.  Dijkstra's algorithm solver
4.  Backtracking depth-first search solver

"""


class MazeRunner:
	def __init__(self,width,height,colors_dict=None):
		self.width = width
		self.height = height
		self.maze = VoronoiMaze(width=self.width,height=self.height)
		if not colors_dict:
			self.colors_dict = {
				"background_color":"#e0e0e0",
				"maze_line_color": "navy",
				"neighbor_line_color": "orange",
				"point_color": "orange",
				"start_color": "blue",
				"exit_color": "red",
				"polygon_face_color": "#1fc600",
				"polygon_edge_color": "none",
				"polygon_backtracking_color": "purple",
				"polygon_backtracking_edge_color": "none"
				}
		else:
			self.colors_dict = colors_dict
		self.generate_animations()

	def generate_animations(self):
		"""generate matplotlib animations for each solver"""
		solvers = [MazeSolverDFS(self.maze), MazeSolverBFS(self.maze), MazeSolverDijkstra(self.maze), MazeSolverBacktracking(self.maze)]
		maze_plot = VoronoiMazePlot(self.maze, colors_dict=self.colors_dict)
		for solver in solvers:
			self.animate_solver(maze_plot,solver)
		return

	def animate_solver(self,maze_plot,solver):
		"""creates a matplotlib animation for the solver, then clears the plot"""
		maze_plot.path = solver.path
		maze_plot.name = solver.name
		print(solver.name)
		maze_plot.animate()
		maze_plot.clear_maze()
		return


if __name__=='__main__':
	MazeRunner(100,100)
