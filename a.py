#!/usr/bin/python
import sys
from PIL import Image
#from __future__ import print_function
import time
print time.strftime('%Y-%m-%d %H:%M:%S')

line_space = 5  # min line space



# main
im = Image.open("a1.jpg")
print(im.format, im.size, im.mode)
out=im.convert("L").point(lambda x: 0 if x<90 else 255).convert("1")
print(out.format, out.size, out.mode)

print type(out.size)

print "x is : ", out.size[0]
print "y is : ", out.size[1]


## Look up the pixel
# pix = out.load()
# for i in xrange(0,out.size[0]-1):
# 	for j in xrange(0,out.size[1]-1):
# 		if pix[i, j]==0:
# 			sys.stdout.write('0')
# 		else:
# 			sys.stdout.write('1')
# 	print	 	


info_rows=[];
pix = out.load()
for y in xrange(0,out.size[1]):
	for x in xrange(0,out.size[0]):
		if pix[x, y]==0:
			info_rows+=[y]
			break

print info_rows
print len(info_rows)
print len(info_rows)-1

info_row_pair = []
info_row_start=info_rows[0]
for i in xrange(1,len(info_rows)):
	print i,
	if info_rows[i] - info_rows[i-1] > line_space :
		info_row_a=info_row_start;
		info_row_b=info_rows[i-1];
		info_row_pair += [[info_row_a,info_row_b]]
		info_row_start=info_rows[i];
	if 	i == (len(info_rows)-1):
		print 'run here'
		info_row_pair += [[info_row_start,info_rows[i]]]

print info_row_pair

for pair in info_row_pair:
	print pair,
	for x in xrange(0,out.size[0]):
		pix[x,pair[0]] = 0
		pix[x,pair[1]] = 0










out.save("b.jpg","JPEG")