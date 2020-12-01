'''
Thresh layers

including : binary thresh and inv_binary thresh

By jzyustc, 2020/11/30

'''

from . import *


class BinaryThreshHold(Module):
	'''
		Binary the Gray image By Thresh
	'''

	def __init__(self, thresh):
		super(BinaryThreshHold, self).__init__()
		self.thresh = thresh

	def forward(self, input: np.ndarray):
		ret, ee = cv2.threshold(input, self.thresh, input.max(), cv2.THRESH_BINARY)
		return ee


class IBinaryThreshHold(Module):
	'''
		Binary the Gray image By Thresh, but color Inverted
	'''

	def __init__(self, thresh):
		super(IBinaryThreshHold, self).__init__()
		self.thresh = thresh

	def forward(self, input: np.ndarray):
		ret, ee = cv2.threshold(input, self.thresh, input.max(), cv2.THRESH_BINARY_INV)
		return ee
