'''
Mapping layers

including : Linear mapping to [0,1], Linear mapping to [0,255] , etc

#TODO : add more kinds of mapping

By jzyustc, 2020/11/30

'''
from . import *


class LinearMap2Mask(Module):
	'''
		Linear Transform an image to a mask
	'''

	def __init__(self, min=0, max=1):
		super(LinearMap2Mask, self).__init__()

		if min < 0 or max > 1 or min > max:
			raise ValueError("Error input of min and max range")

		self.min = min
		self.max = max

	def forward(self, input: np.ndarray):
		input_min = input.min()
		input_max = input.max()

		# all pixels have the same value
		if input_max == input_min: return np.ones(input.shape) * self.max

		# otherwise
		return (input - input_min) / (input_max - input_min) * (self.max - self.min) + self.min


class LinearMap2Image(Module):
	'''
		Linear Transform an image to [min, max]
	'''

	def __init__(self, min=0, max=255):
		super(LinearMap2Image, self).__init__()

		if min < 0 or max > 255 or min > max:
			raise ValueError("Error input of min and max range")

		self.min = min
		self.max = max

	def forward(self, input: np.ndarray):
		input_min = input.min()
		input_max = input.max()

		# all pixels have the same value
		if input_max == input_min: return np.ones(input.shape) * self.max

		# otherwise
		return (input - input_min) / (input_max - input_min) * (self.max - self.min) + self.min
