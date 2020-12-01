'''
Basic transform layers

including : identity, RGB2Gray, Gray2RGB, resize, crop, mask

By jzyustc, 2020/11/29
'''
from . import *
from ..layer.mapping import LinearMap2Image


class Identity(Module):
	'''
		Identity mapping
	'''

	def __init__(self):
		super(Identity, self).__init__()

	def forward(self, *input):
		return input


class RGB2Gray(Module):
	'''
		Transform from RGB to Gray
	'''

	def __init__(self):
		super(RGB2Gray, self).__init__()

	def forward(self, input: np.ndarray):
		if len(input.shape) != 3:
			raise ValueError("Input image is not a RGB image")
		elif input.shape[2] != 3:
			raise ValueError("Input image have " + str(input.shape[2]) + " channels")

		return cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)


class Gray2RGB(Module):
	'''
		Transform from Gray to RGB
	'''

	def __init__(self):
		super(Gray2RGB, self).__init__()

	def forward(self, input: np.ndarray):
		if len(input.shape) != 2:
			raise ValueError("Input image is not a Gray image")

		if input.max() > 255:
			linear_mapping = LinearMap2Image(min=input.min(), max=255)
			input = linear_mapping(input)

		if input.min() < 0:
			linear_mapping = LinearMap2Image(min=0, max=input.max())
			input = linear_mapping(input)

		return np.expand_dims(input, 2).repeat(3, axis=2)


class Resize(Module):
	'''
		Resize the image

		Usage :

		 > Resize((100, 200)) or Resize(shape=(100, 200))

	'''

	def __init__(self, shape: tuple, interpolation=cv2.INTER_LINEAR):
		self.shape = shape
		self.interpolation = interpolation
		super(Resize, self).__init__()

	def forward(self, input: np.ndarray):
		return cv2.resize(input, self.shape, interpolation=self.interpolation)


CROP_CENTER = 0
CROP_RANDOM = 1
CROP_SET = 2


class Crop(Module):
	'''
		Crop the image

		Usage :

		Center Crop : Crop from the center of image, and the width of height is cropped image is $proportion times the original
		 > Crop(0.5, method=CROP_CENTER) or Crop(proportion=0.5, method=CROP_CENTER)

		Random Crop : Random crop image so that the area is $proportion times the original
		 > Crop(0.5, method=CROP_RANDOM) or Crop(proportion=0.5, method=CROP_RANDOM)

		Set Crop : Set crop ranges , as a list:[top, bottom, left, right]
		 > Crop([100,300,200,400], method=CROP_SET) or Crop(range=[100,300,200,400], method=CROP_SET)

	'''

	def __init__(self, *params, method=CROP_CENTER, **kwargs):
		super(Crop, self).__init__()
		self.method = method
		self.params = params
		self.kwargs = kwargs

	def center(self, input: np.ndarray, proportion: float):
		if proportion <= 0 or proportion > 1:
			raise ValueError("Proportion should between (0,1]")
		height, width = input.shape[0:2]
		top = int(0.5 * (1 - proportion) * height)
		bottom = int(0.5 * (1 + proportion) * height)
		left = int(0.5 * (1 - proportion) * width)
		right = int(0.5 * (1 + proportion) * width)
		return input[top:bottom, left:right]

	def random(self, input: np.ndarray, proportion: float):
		if proportion <= 0 or proportion > 1:
			raise ValueError("Proportion should between (0,1]")
		height, width = input.shape[0:2]
		area = width * height * proportion

		# restrict : the width or height of crop area must be larger than pow(area, 0.5) / 2
		# in order to make the crop area more square
		min = int(pow(area, 0.5) / 2)
		while True:
			top = random.randint(1, height - min) - 1
			crop_height = random.randint(min, height - top - 1)
			left = random.randint(0, width - min) - 1
			crop_width = int(area / crop_height)
			if left + crop_width < width:
				return input[top:top + crop_height, left:left + crop_width]

	def set(self, input: np.ndarray, range: [int]):
		if len(range) != 4:
			raise ValueError("Length of range should be 4 : top, bottom, left, right")
		height, width = input.shape[0:2]

		if range[0] < 0 or range[0] >= width:
			raise ValueError("Crop Left value should be in [0, width-1]")
		if range[1] < 0 or range[1] >= width:
			raise ValueError("Crop Right value should be in [0, width-1]")
		if range[1] <= range[0]:
			raise ValueError("Crop Right value should be larger than Left")

		if range[2] < 0 or range[2] >= width:
			raise ValueError("Crop Top value should be in [0, height-1]")
		if range[3] < 0 or range[3] >= width:
			raise ValueError("Crop Bottom value should be in [0, height-1]")
		if range[3] <= range[2]:
			raise ValueError("Crop Bottom value should be larger than Top")

		return input[range[0]:range[1], range[2]:range[3]]

	def forward(self, input: np.ndarray):
		if self.method == CROP_CENTER:
			if "proportion" in self.kwargs:
				proportion = self.kwargs["proportion"]
			elif len(self.params) != 1:
				raise ValueError("Input param should be proportion of center crop")
			else:
				proportion = self.params[0]
			return self.center(input, proportion)

		if self.method == CROP_RANDOM:
			if "proportion" in self.kwargs:
				proportion = self.kwargs["proportion"]
			elif len(self.params) != 1:
				raise ValueError("Input param should be proportion of random crop area")
			else:
				proportion = self.params[0]
			return self.random(input, proportion)

		if self.method == CROP_SET:
			if "range" in self.kwargs:
				range = self.kwargs["range"]
			elif len(self.params) != 1:
				raise ValueError("Input param should be a int list of cropped range")
			else:
				range = self.params[0]
			return self.set(input, range)
