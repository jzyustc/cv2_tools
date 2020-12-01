'''
Mask layers (make masks)

including : low_linear ,etc

By jzyustc, 2020/11/30

'''

from . import *


class MaskBlack(Module):
	'''
		mask an image with black
	'''

	def __init__(self):
		super(MaskBlack, self).__init__()
		self.rgb2gray = Gray2RGB()

	def forward(self, input: np.ndarray, mask: np.ndarray):
		if mask.max() > 1 or mask.min() < 0:
			raise ValueError("Mask's value should be between [0, 1]")
		if len(mask.shape) == 2 and len(input.shape) == 3:
			mask = self.rgb2gray(mask)
		output = input * mask
		return output


class MaskWhite(Module):
	'''
		mask a image with black
	'''

	def __init__(self):
		super(MaskWhite, self).__init__()
		self.rgb2gray = Gray2RGB()

	def forward(self, input: np.ndarray, mask: np.ndarray):
		if mask.max() > 1 or mask.min() < 0:
			raise ValueError("Mask's value should be between [0, 1]")
		if len(mask.shape) == 2 and len(input.shape) == 3:
			mask = self.rgb2gray(mask)
		output = input + (255 - input) * (1 - mask)
		return output
