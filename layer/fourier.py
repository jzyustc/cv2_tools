'''
Fourier Transform layers

including : FT, IFT, Abs

by jzyustc, 2020/11/29

'''

from . import *


class FT(Module):
	'''
		Fourier Transform : input an image, return the complex form of FT
	'''

	def __init__(self):
		super(FT, self).__init__()

	def forward(self, input: np.ndarray):
		if len(input.shape) != 2:
			raise ValueError("FT needs Gray Image as Input")
		f = np.fft.fft2(input)
		fshift = np.fft.fftshift(f)
		return fshift


class IFT(Module):
	'''
		Inverse Fourier Transform : input the complex form of an image, return the raw image
	'''

	def __init__(self):
		super(IFT, self).__init__()

	def forward(self, input: np.ndarray):
		if len(input.shape) != 2:
			raise ValueError("IFT needs Gray Image as Input")
		fshift = np.fft.ifftshift(input)
		img = np.fft.ifft2(fshift)
		img = np.abs(img)
		return img


class Abs(Module):
	'''
		Value Abs of an image, used when you want to show Modulus of an FT image
	'''

	def __init__(self):
		super(Abs, self).__init__()

	def forward(self, input: np.ndarray):
		s = np.abs(input)
		s = s / s.max() * 255
		return s
