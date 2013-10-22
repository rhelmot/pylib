from .. import qnum
from .. import printing
import numbers

class row:
	def __init__(self, *args):
		if len(args) == 1 and 'items' in args[0]:
			self.items = args[0].items
		if len(args) == 1 and isinstance(args[0], str):
			self.items = map(qnum, args[0].replace(',',' ').translate(None, '[](){}').split())
		elif len(args) == 1 and isinstance(args[0], list):
			self.items = map(qnum, args[0])
		else:
			self.items = map(qnum, args)

	def __mul__(self, other):
		if isinstance(other, numbers.Number):
			return row(map(lambda x: x*other, self.items))
		return self

	def __add__(self, other):
		if isinstance(other, row):
			return row([a+b for a,b in zip(self.items, other.items)])
		return self

	def __sub__(self, other):
		if isinstance(other, row):
			return row([a-b for a,b in zip(self.items, other.items)])
		return self
	
	def __rsub__(self, other):
		if isinstance(other, row):
			return row([b-a for a,b in zip(self.items, other.items)])
	
	def __str__(self):
		return '[' + ', '.join(map(str, self.items)) + ']'
	
	def __repr__(self):
		return 'row(' + str(self) + ')'

	def __len__(self):
		return len(self.items)

	def __getitem__(self, key):
		return self.items[key]

	def __setitem__(self, key, value):
		self.items[key] = value

	def __delitem__(self, key):
		del self.items[key]

	def __iter__(self):
		return iter(self.items)

	def __reversed__(self):
		return reversed(self.items)

	def __contains__(self, item):
		return item in self.items

	def __setslice__(self, i, j, sequence):
		self.items[i:j] = sequence

	def __delslice__(self, i, j):
		del self.items[i:j]

class system:
	def __init__(self, *args):
		if len(args) == 1 and isinstance(args[0], str):
			self.rows = map(row, args[0].split('\n'))
		elif len(args) == 1 and isinstance(args[0], list):
			self.rows = map(row, args[0])
		else:
			self.rows = map(row, args)
		if not all((len(x) == len(self.rows[0])) for x in self.rows):
			raise ValueError('All rows must be same length')

	def rowop_multiply(self, rownum, factor):
		if rownum >= len(self.rows) or rownum < 0:
			raise ValueError('Row number out of bounds')
		self.rows[rownum] *= factor

	def rowop_swap(self, row1, row2):
		if row1 >= len(self.rows) or row2 >= len(self.rows) or row1 < 0 or row2 < 0:
			raise ValueError('Row number out of bounds')
		swap = self.rows[row1]
		self.rows[row1] = self.rows[row2]
		self.rows[row2] = swap

	def rowop_add(self, destrow, srcrow, factor=1):
		tfactor = qnum(factor)
		if destrow >= len(self.rows) or srcrow >= len(self.rows) or destrow < 0 or srcrow < 0:
			raise ValueError('Row number out of bounds')
		self.rows[destrow] += self.rows[srcrow]*tfactor

	def column(self, colnum):
		if colnum >= len(self.rows[0]) or colnum < 0:
			raise ValueError('Column number out of bounds')
		return map(lambda x: x[colnum], self.rows)

	def __str__(self):
		return ',\n'.join(map(str, self.rows))

	def __repr__(self):
		return 'system(\n' + str(self) + ')'

	def echelon(self):
		row = 0
		col = 0
		while row < len(self.rows) and col < len(self.rows[0]):
			tcol = self.column(col)
			if tcol[row:] == [0]*(len(self.rows)-row):
				col += 1
				continue
			if tcol[row+1:] == [0]*(len(self.rows)-(row+1)):
				row += 1
				col += 1
				continue
			if self.rows[row][col] == 0:
				trow = row
				while True:
					trow += 1
					if self.rows[trow][col] != 0:
						break
				self.rowop_swap(row, trow)
				continue
			trow = row
			while True:
				trow += 1
				if self.rows[trow][col] != 0:
					break
			self.rowop_add(trow, row, -1*self.rows[trow][col]/self.rows[row][col])

	def pivots(self):
		row = 0
		col = 0
		while row < len(self.rows) and col < len(self.rows[0]):
			while col < len(self.rows[0]) and self.rows[row][col] == 0:
				col += 1
			if col >= (len(self.rows[0]) - 1):
				break
			yield (row, col)
			row += 1

	def reduce(self):
		self.echelon()
		for row, col in reversed(list(self.pivots())):
			self.rowop_multiply(row, 1/self.rows[row][col])
			for trow in range(row):
				self.rowop_add(trow, row, -1*self.rows[trow][col]/self.rows[row][col])

	def solve(self):
		self.reduce()
		row = 0
		col = 0
		out = {}
		while row < len(self.rows) and col < (len(self.rows[0]) - 1):
			if self.rows[row][col] == 1:
				its = []
				if self.rows[row][-1] != 0:
					its.append(str(self.rows[row][-1]))
				for tcol in range(col+1, len(self.rows[0]) - 1):
					if not self.rows[row][tcol] == 0:
						its.append(str(-1*self.rows[row][tcol]) + 'x' + str(tcol+1))
				out['x' + str(col+1)] = printing.formatsum(its)
				row += 1
			elif self.rows[row][col] == 0:
				out['x' + str(col+1)] = 'free'
			else:
				print 'malformed column for x'+str(col+1)+'?'
			col += 1
		return out
