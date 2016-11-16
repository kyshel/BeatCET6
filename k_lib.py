#!/usr/bin/python

import sys
import pytesseract
from pprint import pprint
from PIL import Image,ImageDraw,ImageChops
import tesserocr
import time

#from __future__ import print_function

class MarkColor:
	def __init__(self,r,g,b,r_bias,g_bias,b_bias):
		self.r=r
		self.g=g
		self.b=b
		self.r_bias=r_bias
		self.g_bias=g_bias
		self.b_bias=b_bias

def print_mark_sample_rgb(mark_sample_path):
	mark_sample = Image.open(mark_sample_path)
	print(mark_sample.format, mark_sample.size, mark_sample.mode)
	r,g,b=[],[],[]
	get_rgb_list(mark_sample,r,g,b)
	for i in r,g,b:
		print 'max:',max(i),
		print 'min:',min(i),
		print 'avg:',sum(i)/len(i),
		print 'bias_x(max-avg):',max(i)-sum(i)/len(i),
		print 'bias_y(avg-min):',sum(i)/len(i)-min(i)

def print_pixel(image):
	pixel = image.load()
	for i in xrange(0,image.size[0]-1):
		for j in xrange(0,image.size[1]-1):
			print pixel[i,j]

def get_rows(image):
	rows=[];
	pixel = image.load()
	for y in xrange(0,image.size[1]):
		for x in xrange(0,image.size[0]):
			#print pixel[x, y],
			if pixel[x, y]==0:
				rows+=[y]
				break
	return rows



def get_pairs(infos,distance):
	pairs = []
	start=infos[0]
	for i in xrange(1,len(infos)):
		if infos[i] - infos[i-1] > distance :
			a=start;
			b=infos[i-1];
			pairs += [[a,b]]
			start=infos[i];
		if 	i == (len(infos)-1):
			#print 'run here'
			pairs += [[start,infos[i]]]
	return pairs


def get_cols(image,row_pairs):
	cols=[]	
	pixel = image.load()
	for row_pair in row_pairs:
		col_line=[]
		for x in xrange(0,image.size[0]):
			for y in xrange(row_pair[0],row_pair[1]+1):
				#print x,y,pixel[x, y]
				if pixel[x, y]==0:
					col_line += [x]
					break
		#print col_line
		cols+=[col_line]

	return cols




def add_row_line(image,row_pairs):
	pixel = image.load()
	for pair in row_pairs:
		for x in xrange(0,image.size[0]):
			pixel[x,pair[0]] = 0
			pixel[x,pair[1]] = 0
	return

def get_mark(image,c):
	image_mark = Image.new("RGB", (image.size[0], image.size[1]),"white")
	image_demark = image.copy()
	pixel = image.load()
	pixel_mark = image_mark.load()
	pixel_de_mark = image_demark.load()

	for i in xrange(0,image.size[0]):
		for j in xrange(0,image.size[1]):
			if  c.r - c.r_bias < pixel[i,j][0] < c.r + c.r_bias :
				if c.g - c.g_bias < pixel[i,j][1] < c.g + c.g_bias :
					if c.b - c.b_bias < pixel[i,j][2] < c.b + c.b_bias :
						pixel_mark[i,j] = pixel[i,j]
						pixel_de_mark[i,j] = (255,255,255)

	#return image_mark,image_demark
	return {'mark':image_mark, 'demark':image_demark}


def get_rgb_list(image,r,g,b):
	pixel = image.load()
	for i in xrange(0,image.size[0]):
		for j in xrange(0,image.size[1]):
			r+=[pixel[i,j][0]]
			g+=[pixel[i,j][1]]
			b+=[pixel[i,j][2]]


def get_crops(row_pairs,col_pairs):
	line = 0
	
	crops=[]
	for row_pair in row_pairs:
		crops_line = []
		for col_pair in col_pairs[line]:
			crop= [col_pair[0],row_pair[0],col_pair[1],row_pair[1]]
			crops_line += [crop]
		line = line + 1		
		crops += [crops_line]

	return crops



def get_line_height(row_pairs):
	pairs_span = []
	for pairs in row_pairs:
		pairs_span += [pairs[1]-pairs[0]]

	pairs_span.sort()
	# for item in pairs_span:
	# 	print item

	#return sum(pairs_span)/len(pairs_span) # take avg
	return pairs_span[len(pairs_span)/2] # take median


def draw_rectangle(image,crops):
	image_copy=image.copy()
	draw = ImageDraw.Draw(image_copy)
	for crops_line in crops:
		#print crops_line
		for crop in crops_line:
			draw.rectangle(crop,outline="black")
	return image_copy

def draw_rectangle2(image,crops): 
	image_copy=image.copy()
	draw = ImageDraw.Draw(image_copy)
	for crop in crops:
		draw.rectangle(crop,outline="black")
	return image_copy


def calc_crops(image,threshold,line_height_word_space_ratio):
	denoise=image.convert("L").point(lambda x: 0 if x < threshold else 255).convert("1")
	print 'denoise:',(denoise.format, denoise.size, denoise.mode)

	rows=get_rows(denoise)
	row_pairs=get_pairs(rows,1)

	line_height=get_line_height(row_pairs)
	word_space = line_height / line_height_word_space_ratio
	print 'line_height:',line_height
	print 'word_space:',word_space

	cols=get_cols(denoise,row_pairs)
	#pprint (cols)
	col_pairs=[]
	for col_line in cols:
		#print col_line
		col_line_pairs=get_pairs(col_line,word_space)
		col_pairs+=[col_line_pairs]

	crops = get_crops(row_pairs,col_pairs)


	return crops,line_height


def calc_crops2(image,threshold,line_height,line_height_word_space_ratio):
	denoise=image.convert("L").point(lambda x: 0 if x < threshold else 255).convert("1")
	print 'denoise:',(denoise.format, denoise.size, denoise.mode)

	rows=get_rows(denoise)
	if rows == []:
		print 'WARNING: no info in this image!'
		return
	row_pairs=get_pairs(rows,1)

	word_space = line_height / line_height_word_space_ratio
	print 'line_height:',line_height
	print 'word_space:',word_space

	cols=get_cols(denoise,row_pairs)
	#pprint (cols)
	col_pairs=[]
	for col_line in cols:
		#print col_line
		col_line_pairs=get_pairs(col_line,word_space)
		col_pairs+=[col_line_pairs]

	crops = get_crops(row_pairs,col_pairs)

	return crops

def get_white_copy(image):
	copy = Image.new("1", (image.size[0], image.size[1]),"white")
	return copy

def filter_marked_words(image,crops):
	template=get_white_copy(image)
	for box in crops:
		template.paste(demark_denoise.crop(box), box)
	return template

def list_marked_words(image,crops,line_height):
	template=get_white_copy(image)
	i=0
	for box in crops:
		position=(20,i*line_height+20)
		template.paste(demark_denoise.crop(box),position )
		i=i+1
	return template

def get_crops_truncate(crops,image):
	for crop in crops:
		crop[3]=get_crop_truncate_line(crop,image)
	return crops
		

def get_crop_truncate_line(crop,image):	
	pixel = image.load()
	for y in xrange((crop[1]+crop[3])/2,crop[3]+1):
		for x in xrange(crop[0],crop[2]+1):
			if pixel[x, y]==0:
				break
			if x == crop[2]:
				#print 'xxxxxxxxxxxxxxxxxxxxx'
				cut_line = y + 1
				return cut_line
	return crop[3] # won't excute as common
