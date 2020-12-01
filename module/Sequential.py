'''
Sequential Layers Composer

By jzyustc, 2020/11/29

'''
from . import *
from collections import OrderedDict


class Sequential(Module):
	def __init__(self, layers=None):
		super(Sequential, self).__init__()
		if layers is None:
			layers = OrderedDict([])
		self.layers = layers

	def forward(self, input):
		'''
		forward function of the layers

		:param input:
		:return:
		'''
		output = input
		for name, layer in self.layers.items():
			output = layer(output)
		return output

	def append(self, *input):
		'''
		append items into self.layers

		:param input:
		:return:
		'''
		if len(input) != 1:
			raise TypeError("Input are illegal")

		if type(input[0]) == OrderedDict:
			self.append_ordered_dict(input[0])
		elif type(input[0]) == list:
			self.append_list(input[0])
		elif issubclass(input[0].__class__, Module):
			self.append_module(input[0])
		else:
			raise TypeError("Input are illegal")

	def append_ordered_dict(self, append: OrderedDict):
		'''
		append with OrderedDict

		:param append:
		:return:
		'''
		for name, mod in append.items():

			if type(name) != str:
				raise NameError("Name of module is not a string")
			elif not issubclass(mod.__class__, Module):
				raise ValueError("Added part is not subclass of Module")
			elif self.layers.get(name) != None:
				raise NameError("Name of module has exist")

			self.layers[name] = mod

	def append_list(self, append: [Module]):
		'''
		append with a list of Module

		:param append:
		:return:
		'''
		for mod in append:
			self.append(mod)

	def append_module(self, append: Module):
		'''
		append with one Module

		:param append:
		:return:
		'''
		if append.__class__.__base__ != Module:
			raise ValueError("Added part is not subclass of Module")

		name = append.__class__.__name__ + "_"

		id = 0
		while self.layers.get(name + str(id)) is not None:
			id += 1
		name += str(id)

		self.layers[name] = append

	def get_layers(self):
		return self.layers
