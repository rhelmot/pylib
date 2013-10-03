from fractions import Fraction, gcd
from decimal import Decimal

prec = 4

def qnum(a=0, b=1):
	if isinstance(a, str):
		a = Decimal(a)
	if isinstance(b, str):
		b = Decimal(b)
	if isinstance(a, Decimal) or isinstance(b, Decimal) or isinstance(a, Fraction) or isinstance(b, Fraction):
		return Fraction(a/b)
	elif isinstance(a, float) and isinstance(b, float):
		return Fraction(Decimal(str(a))/Decimal(str(b)))
	elif isinstance(a, float):
		return Fraction(Decimal(str(a)/b))
	elif isinstance(b, float):
		return Fraction(a/Decimal(str(b)))
	else:
		return Fraction(a,b)


import linalg
