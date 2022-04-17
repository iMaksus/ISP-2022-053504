from abc import ABC, abstractclassmethod

class BaseSerializator(ABC):
	# convert Python object to file
	@abstractclassmethod
	def dump(self):
		pass

	# convert Python object to string
	@abstractclassmethod
	def dumps(self):
		pass

	# converts file to Python object
	@abstractclassmethod
	def load(self):
		pass

	# converts string to Python object
	@abstractclassmethod
	def loads(self):
		pass