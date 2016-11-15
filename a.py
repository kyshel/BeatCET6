#!/usr/bin/python
# >>>>>>>>>>>>>>>>>>>> preload <<<<<<<<<<<<<<<<<<<<<<<<<<<
execfile("k_lib.py")
print '>>>>>>>>>>>>>>>',time.strftime('%Y-%m-%d %H:%M:%S'),'<<<<<<<<<<<<<<<<'


# >>>>>>>>>>>>>>>>>>>> config <<<<<<<<<<<<<<<<<<<<<<<<<<<
origin_path="a1.jpg"

# - recommend,rgb:121,32,40; bias:10; hereshold:100; ratio:4
r,g,b=127,32,40
bias=40
threshold=100
line_height_word_space_ratio = 4
#line_height_line_space_ratio = 8
#line_height_letter_space_ratio = 50

# - get mark sample rgb
# mark_sample_path="a_m2.jpg"
# print_mark_sample_rgb(mark_sample_path)



# >>>>>>>>>>>>>>>>>>>> main <<<<<<<<<<<<<<<<<<<<<<<<<<<
origin = Image.open(origin_path)
print 'origin:',(origin.format, origin.size, origin.mode)
#print_pixel(origin)
#mark_color=MarkColor(121,32,40,bias,bias,bias)
mark_color=MarkColor(r,g,b,bias,bias,bias)

result=get_mark(origin,mark_color) # time waste
mark=result['mark']
de_mark=result['de_mark']
mark.convert("").save("mark.jpg","JPEG")
de_mark.convert("").save("de_mark.jpg","JPEG")

denoised=de_mark.convert("L").point(lambda x: 0 if x < threshold else 255).convert("1")
print 'denoised:',(denoised.format, denoised.size, denoised.mode)

rows=get_rows(denoised)
row_pairs=get_pairs(rows,1)

line_height=get_line_height(row_pairs)
word_space = line_height / line_height_word_space_ratio
print 'line_height:',line_height
print 'word_space:',word_space

cols=get_cols(denoised,row_pairs)
#pprint (cols)
col_pairs=[]
for col_line in cols:
	#print col_line
	col_line_pairs=get_pairs(col_line,word_space)
	col_pairs+=[col_line_pairs]



crops = get_crops()
draw_rectangle(denoised,crops)

denoised.save("cropped.jpg","JPEG")







