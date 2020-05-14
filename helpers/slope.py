"""
Helper class to calculate intercepts for Voronoi cell edges that are outside of the 
boundary box.
"""

class BoundingBoxIntercepts:
	def __init__(self,p1,p2):
		self.p1 = p1
		self.p2 = p2
		self.slope = self.calculate_slope()
		self.intercept = self.get_y_intercept()
		self.top = self.get_top_bound()
		self.bottom = self.get_bottom_bound()
		self.left = self.get_left_bound()
		self.right = self.get_right_bound()

	def calculate_slope(self):
		return (self.p2[1]-self.p1[1]) / (self.p2[0]-self.p1[0])

	def get_y_intercept(self):
		intercept = self.p2[1] - (self.slope * self.p2[0])
		return intercept

	def get_top_bound(self):
		y = 100
		x = (y-self.intercept) / self.slope
		return x

	def get_right_bound(self):
		x = 100
		y = (self.slope * x) + self.intercept
		return y

	def get_left_bound(self):
		x = 0
		y = self.intercept
		return y

	def get_bottom_bound(self):
		y = 0
		x = (y-self.intercept) / self.slope 
		return x	





