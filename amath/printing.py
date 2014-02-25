def formatsum(items):
	out = ''
	items = map(str, items)
	for i in items:
		if i == 'None' or i == '' or i[0] == '0':
			continue
		if i[0] == '-':
			if out == '':
				out += i
			else:
				out += ' - ' + i[1:]
		else:
			if i[0] == '+':
				i = i[1:]
			if out == '':
				out += i
			else:
				out += ' + ' + i
	return out if not out=='' else '0'
