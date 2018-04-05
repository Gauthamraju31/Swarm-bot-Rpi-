import numpy as np

class Object:

	def __init__(self):

		self.x_pos = 0
		self.y_pos = 0
		self.img_x = 0
		self.img_y = 0
		self.old_x_pos = 0
		self.old_y_pos = 0
		self.HSV_Upper = np.array([0,0,0])
		self.HSV_Lower = np.array([0,0,0])

	def set_x_pos(self,x):
		self.old_x_pos = self.x_pos
		self.x_pos = x

	def get_x_pos(self):
		return self.x_pos

	def set_img_x(self,x):
		self.img_x = x

	def get_img_x(self):
		return self.img_x

	def get_old_x(self):
		return self.old_x_pos

	def set_y_pos(self,y):
		self.old_y_pos = self.y_pos
		self.y_pos = y

	def get_y_pos(self):
		return self.y_pos

	def set_img_y(self,y):
		self.img_y = y

	def get_img_y(self):
		return self.img_y

	def get_old_y(self):
		return self.old_y_pos

	def setHSVlower(self, lower):
		self.HSV_Lower = np.array(lower)

	def setHSVupper(self, upper):
		self.HSV_Upper = np.array(upper)

	def getHSVupper(self):
		return self.HSV_Upper

	def getHSVlower(self):
		return self.HSV_Lower


