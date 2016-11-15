#!/usr/bin/python

import sys
from pprint import pprint
from PIL import Image,ImageDraw
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
			for y in xrange(row_pair[0],row_pair[1]):
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
	pixel = image.load()
	pixel_mark = image_mark.load()

	for i in xrange(0,image.size[0]):
		for j in xrange(0,image.size[1]):
			if  c.r - c.r_bias < pixel[i,j][0] < c.r + c.r_bias :
				if c.g - c.g_bias < pixel[i,j][1] < c.g + c.g_bias :
					if c.b - c.b_bias < pixel[i,j][2] < c.b + c.b_bias :
						pixel_mark[i,j] = pixel[i,j]
	return image_mark

def get_rgb_list(image,r,g,b):
	pixel = image.load()
	for i in xrange(0,image.size[0]):
		for j in xrange(0,image.size[1]):
			r+=[pixel[i,j][0]]
			g+=[pixel[i,j][1]]
			b+=[pixel[i,j][2]]


def get_crops():
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