'''
Filter layers

including : rect ideal filter, round ideal filter, Butterworth filter, Gaussian filter

By jzyustc, 2020/11/29

'''
from . import *

FILTER_IDEAL = 0
FILTER_BUTTERWORTH = 1
FILTER_GAUSSIAN = 2


class RoundFilter(Module):
	'''
		Filters that based on a round area
	'''

	allowed_modes = [FILTER_IDEAL, FILTER_BUTTERWORTH, FILTER_GAUSSIAN]

	def __init__(self, size: float, mode=FILTER_GAUSSIAN, is_high=False, n=2):
		super(RoundFilter, self).__init__()

		if mode not in self.allowed_modes:
			raise ValueError("Not Allowed Mode in Filter")
		self.mode = mode
		self.is_high = is_high
		self.n = n
		self.radius = size

	def mask(self, input: np.ndarray):

		shape = input.shape
		rows, cols = shape[:2]
		r, c = np.mgrid[0:rows:1, 0:cols:1]

		c -= int(cols / 2)
		r -= int(rows / 2)
		d = np.power(c, 2.0) + np.power(r, 2.0)
		if self.mode == FILTER_IDEAL:
			lpFilter = np.zeros(shape[:2])
			lpFilter[lpFilter < pow(self.radius, 2.0)] = 1
		elif self.mode == FILTER_BUTTERWORTH:
			lpFilter = 1.0 / (1 + np.power(np.sqrt(d) / self.radius, 2 * self.n))
		elif self.mode == FILTER_GAUSSIAN:
			lpFilter = np.exp(-d / (2 * pow(self.radius, 2.0)))
		else:
			raise ValueError("Unknown Mode")
		return lpFilter

	def forward(self, input: np.ndarray):
		if len(input.shape) != 2:
			raise ValueError("Filter needs Gray Input")

		mask = self.mask(input)
		if self.is_high: mask = 1 - mask

		return input * mask


class RectFilter(Module):
	'''
		Filters that based on a Rectangle area
	'''

	allowed_modes = [FILTER_IDEAL]

	def __init__(self, size: int, mode=FILTER_IDEAL, is_high=False):
		super(RectFilter, self).__init__()
		if mode not in self.allowed_modes:
			raise ValueError("Not Allowed Mode in Filter")
		self.mode = mode

		self.size = size
		self.is_high = is_high

	def forward(self, input: np.ndarray):
		if len(input.shape) != 2:
			raise ValueError("Filter needs Gray Input")

		height, width = input.shape[:2]
		mask = np.zeros(input.shape, np.uint8)
		mask[int(height / 2) - self.size:int(height / 2) + self.size,
		int(width / 2) - self.size:int(width / 2) + self.size] = 1
		if self.is_high: mask = 1 - mask

		return input * mask
