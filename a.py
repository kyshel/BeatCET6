#!/usr/bin/python
execfile("k_lib.py")
print '>>>>>>>>>>>>>>>',time.strftime('%Y-%m-%d %H:%M:%S'),'<<<<<<<<<<<<<<<<'

line_height_word_space_ratio = 3
#line_height_line_space_ratio = 0.5
#line_height_letter_space_ratio = 1

# >>>>>>>>>>>>>>>>>>>> main <<<<<<<<<<<<<<<<<<<<<<<<<<<
origin = Image.open("a1.jpg")
print(origin.format, origin.size, origin.mode)
# #print_pixel(origin)
# bias=40
# mark_color=MarkColor(121,32,40,bias,bias,bias)
# mark=get_mark(origin,mark_color)
# mark.convert("").save("mark.jpg","JPEG")

threshold=origin.convert("L").point(lambda x: 0 if x<90 else 255).convert("1")
print(threshold.format, threshold.size, threshold.mode)

rows=get_rows(threshold)
row_pairs=get_pairs(rows,1)
# print rows
# print row_pairs

line_height=get_line_height(row_pairs)
word_space = line_height / line_height_word_space_ratio

print line_height
print word_space

cols=get_cols(threshold,row_pairs)
col_pairs=[]
for col_line in cols:
	col_line_pairs=get_pairs(col_line,word_space)
	col_pairs+=[col_line_pairs]
# print(cols)
# pprint(col_pairs)

# add_row_line(threshold,row_pairs)

crops = get_crops()

draw = ImageDraw.Draw(threshold)
for crops_line in crops:
	#print crops_line
	for crop in crops_line:
		draw.rectangle(crop,outline="black")





threshold.save("b.jpg","JPEG")




# # get avg rgb, only for a_m2.jpg
# mark_sample = Image.open("a_m2.jpg")
# print(mark_sample.format, mark_sample.size, mark_sample.mode)
# r,g,b=[],[],[]
# get_rgb_list(mark_sample,r,g,b)
# for i in r,g,b:
# 	#print i
# 	print 'max:',max(i),'min:',min(i),'avg:',sum(i)/len(i)
