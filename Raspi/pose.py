

class Pose:

	def __init__(self, x = 0.0,y = 0.0,theta=0.0):

		self.x = x
		self.y = y
		self.theta = theta

	def getPose(self):
		return (self.x, self.y, self.theta)

	def setPose(self,x,y,theta):

		self.x = x
		self.y = y
		self.theta = theta
