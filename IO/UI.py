'''
UI

By jzyustc, 2020/11/30

'''

from . import *


def nothing(args):
	pass


class ParamsAdjustUI():

	def __init__(self):
		self.raw_image = None
		self.transformed_image = None
		self.transform_function = None

	def create_trackbar(self, trackWindowName="tracks"):
		'''
			Create a Trackbar Window to control params
		'''
		cv2.namedWindow(trackWindowName)
		self.trackWindowName = trackWindowName
		self.trackbarNames = []

	def add_track_bar(self, trackbarName: str, value, count, onChange=None):
		'''
			Add a Trackbar to the Trackbar Window
		'''
		if onChange is None:
			onChange = nothing
		cv2.createTrackbar(trackbarName, self.trackWindowName, value, count, onChange)
		self.trackbarNames.append(trackbarName)

	def get_track_bar_value(self, trackbarName: str):
		'''
			Return value of a Trackbar from the Trackbar Window
		'''
		if trackbarName not in self.trackbarNames:
			raise ValueError("TrackBar not added")
		return cv2.getTrackbarPos(trackbarName, self.trackWindowName)

	def read_raw_image(self, path):
		'''
			Read image from path
		'''
		self.raw_image = read_image(path)

	def save_transformed_image(self, path):
		'''
			Save transformed image to the path
		'''
		write_image(path, self.transformed_image)

	def get_transform_function(self, trans_func):
		'''
			Get transform function
		'''
		self.transform_function = trans_func

	def transform(self):
		'''
			Transform
		'''
		self.transformed_image = self.transform_function(self.raw_image)

	def show(self, show_raw=True, show_transformed=True):
		'''
			Show the images
		'''
		if show_raw: cv2.imshow("raw_image", self.raw_image)
		if show_transformed: cv2.imshow("transformed_image", np.uint8(self.transformed_image))

	def show_with_params_control(self):
		'''
			Show images with Trackbar Controller, press esc to quit
		'''
		while True:
			self.transform()
			self.show()
			key = cv2.waitKey(1)
			if key == 27:
				break
		cv2.destroyAllWindows()
