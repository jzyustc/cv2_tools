'''
Contour finding layers

including : basic erode, Fuzzy erosion

By jzyustc, 2020/11/30

'''
from . import *


class ContourMask(Module):
	'''
		Find Contours of the image, and fill areas insides to make a mask
	'''

	def __init__(self, thresh):
		super(ContourMask, self).__init__()
		self.thresh = thresh

	def forward(self, input: np.ndarray):
		ret, ee = cv2.threshold(input, self.thresh, input.max(), cv2.THRESH_BINARY_INV)

		contours, hierarchy = cv2.findContours(ee, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

		mask = np.ones((input.shape[0], input.shape[1], 3)) * 255
		for i in range(len(contours)):
			cv2.fillConvexPoly(mask, contours[i], (0, 0, 0))

		return mask


class BoxContourMask(Module):
	'''
		Find the Box Contours of the image, and fill these areas(larger than min_area) to make a mask
	'''

	def __init__(self, thresh, min_area):
		super(BoxContourMask, self).__init__()
		self.thresh = thresh
		self.min_area = min_area

	def forward(self, input: np.ndarray):
		ret, ee = cv2.threshold(input, self.thresh, input.max(), cv2.THRESH_BINARY_INV)

		contours, hierarchy = cv2.findContours(ee, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

		region = []
		for i in range(len(contours)):
			cnt = contours[i]
			area = cv2.contourArea(cnt)
			if (area < self.min_area): continue
			rect = cv2.minAreaRect(cnt)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			region.append(box)

		mask = np.ones((input.shape[0], input.shape[1], 3)) * 255
		for box in region:
			cv2.fillConvexPoly(mask, box, (0, 0, 0))

		return mask
