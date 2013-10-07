from . import linalg

class vector(linalg.systems.row):
	def __getattr__(self, key):
		if len(key) == 1:
			i = ord(key)
			if i >= ord('x'):
				i -= ord('x')
			elif i >= ord('a'):
				i -= ord('a')
		elif key[:1].isdigit():
			i = int(key[:1])
		else:
			raise KeyError(key)
		print self
		return self.items[i]
	
	def __repr__(self):
		return 'vector(' + str(self) + ')'

	def __coerce__(self, other):
		if isinstance(other, list):
			return (self.items, other)
#		elif isinstance(other, linalg.systems.row):
#			return (linalg.systems.row(self.items), other)
		return None
	
	def __mul__(self, other):
		return vector(super(self, other))
	
	def dot(self, other):
		pass
	
	def cross(self, other):
		pass

