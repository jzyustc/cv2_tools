'''
Erode transform layers

including : basic erode, Fuzzy erosion

By jzyustc, 2020/11/30

'''

from . import *


class Erode(Module):
	'''
		Erode the image
	'''

	def __init__(self, kernel_size):
		super(Erode, self).__init__()
		self.kernel_size = kernel_size

	def forward(self, input: np.ndarray):
		kernel = np.ones(self.kernel_size, np.uint8)
		return cv2.erode(input, kernel)
