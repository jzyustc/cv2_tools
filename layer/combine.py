'''
Combine layers, using the single basic layer to combine useful layers

By jzyustc, 2020/12/1

'''

from . import *


class ErodeMaskFuzzy(Module):
	'''
		Erode the image and apply a Gaussian low_freq filter to turn fuzzy
	'''

	def __init__(self, kernel_size, filter_size, mode=FILTER_GAUSSIAN, is_high=False, n=2):
		super(ErodeMaskFuzzy, self).__init__()
		self.kernel_size = kernel_size
		self.low_pass = LowPass(filter_size, mode=mode, is_high=is_high, n=n)

	def forward(self, input: np.ndarray):
		kernel = np.ones(self.kernel_size, np.uint8)

		img = cv2.erode(input, kernel)

		img = self.low_pass(img)

		return img


class LowPass(Module):

	def __init__(self, filter_size, mode=FILTER_GAUSSIAN, is_high=False, n=2):
		super(LowPass, self).__init__()
		self.ft = FT()
		self.filter = RoundFilter(size=filter_size, mode=mode, is_high=is_high, n=n)
		self.ift = IFT()

	def forward(self, input: np.ndarray):
		img = self.ift(self.filter(self.ft(input)))
		return img
