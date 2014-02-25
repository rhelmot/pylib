#!/usr/bin/python

out_header = 'DMAC-ABCDEFG\xFF'
in_header = 'goodness we got it right'

import struct, sys, hashlib, getpass, os

def main(args):
	args = args[1:]
	if args[0] == '-k':
		key = args[1]
		args = args[2:]
	else:
		key = getpass.getpass('Encryption key: ')
		if not key == getpass.getpass('Verify key: '):
			print "They don't match!"
			return 1
	if len(args) < 1:
		print 'Specify a file!'
	outfile = None
	try:
		fp = open(args[0])
		if fp.read(len(out_header)) == out_header:
			doenc = False
		else:
			doenc = True
			outfile = args[0] + '.dmas'
			fp.seek(0)
	except:
		print "Bad infile!"
		return 1
	infile = args[0]
	if len(args) > 1:
		outfile = args[1]
	key_r, key_w = os.pipe()
	os.write(key_w, key + '\n')
	os.close(key_w)
	in_r, in_w = os.pipe()
	out_r, out_w = os.pipe()
	if doenc:
		os.write(in_w, in_header + struct.pack('H', len(infile)) + infile + fp.read())
		os.close(in_w)
		os.system('openssl aes-256-cbc -e -pass fd:%d >&%d <&%d' % (key_r, out_w, in_r))
		os.close(out_w)

		fo = open(outfile,'w')
		fo.write(out_header)
		while True:
			dis = os.read(out_r, 4096)
			if dis == '':
				break
			fo.write(dis)
		os.close(out_r)
		fo.close()
	else:
		os.write(in_w, fp.read())
		os.close(in_w)
		os.system('openssl aes-256-cbc -d -pass fd:%d >&%d <&%d' % (key_r, out_w, in_r))
		os.close(out_w)
		
		if os.read(out_r, len(in_header)) != in_header:
			print 'Bad key!'
			return 1
		first = os.read(out_r, 2)
		nlen = struct.unpack('H', first)[0]
		doutfile = os.read(out_r, nlen)
		if outfile is None:
			outfile = doutfile
		fo = open(outfile,'w')
		while True:
			dis = os.read(out_r, 4096)
			if dis == '':
				break
			fo.write(dis)
		os.close(out_r)
		fo.close()

def usage():
	print """Do Me A Security -- Andrew's basic encryption program

Usage: dmas [-k key] infile [outfile]"""

if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()
	else:
		sys.exit(main(sys.argv))
