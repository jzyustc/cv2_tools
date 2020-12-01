'''
Base Class of all Modules

By jzyustc, 2020/11/29

'''


class Module(object):

	def __init__(self):
		pass

	def __call__(self, *input, **kwargs):
		return self.forward(*input, **kwargs)

	def forward(self, *input, **kwargs):
		raise NotImplementedError
