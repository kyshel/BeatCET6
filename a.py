#!/usr/bin/python
# >>>>>>>>>>>>>>>>>>>> preload <<<<<<<<<<<<<<<<<<<<<<<<<<<
execfile("k_lib.py")
print '>>>>>>>>>>>>>>>',time.strftime('%Y-%m-%d %H:%M:%S'),'<<<<<<<<<<<<<<<<'

# >>>>>>>>>>>>>>>>>>>> config <<<<<<<<<<<<<<<<<<<<<<<<<<<
origin_path="a5.jpg"

# - recommend,rgb:121,32,40; bias:10; hereshold:100; ratio:4
r,g,b=127,32,40
bias=40

threshold=90
line_height_word_space_ratio = 4
#line_height_line_space_ratio = 8
#line_height_letter_space_ratio = 50

## - get mark sample rgb
# mark_sample_path="a_m2.jpg"
# print_mark_sample_rgb(mark_sample_path)

# >>>>>>>>>>>>>>>>>>>> main <<<<<<<<<<<<<<<<<<<<<<<<<<<
origin = Image.open(origin_path)
print 'origin:',(origin.format, origin.size, origin.mode)
mark_color=MarkColor(r,g,b,bias,bias,bias)

result=get_mark(origin,mark_color) # time waste
demark=result['demark']
mark=result['mark']
demark_denoise=demark.convert("L").point(lambda x: 0 if x < threshold else 255).convert("1")
mark_denoise=mark.convert("L").point(lambda x: 0 if x < threshold else 255).convert("1")

demark.save("demark.jpg","JPEG")
mark.save("mark.jpg","JPEG")
demark_denoise.save("demark_denosie.jpg","JPEG")
mark_denoise.save("mark_denoise.jpg","JPEG")

crops_demark,line_height=calc_crops(demark,threshold,line_height_word_space_ratio)
draw_rectangle(demark,crops_demark).save("demark_cropped.jpg","JPEG")
draw_rectangle(demark_denoise,crops_demark).save("demark_cropped_denoise.jpg","JPEG")

crops_mark=calc_crops2(mark,threshold,line_height,line_height_word_space_ratio)
draw_rectangle(mark,crops_mark).save("mark_cropped.jpg","JPEG")
draw_rectangle(mark_denoise,crops_mark).save("mark_cropped_denoise.jpg","JPEG")

points_mark=[] # get mark points
for crops_line in crops_mark:
	for crop in crops_line:
		#print crop
		points_mark += [[(crop[0]+crop[2])/2,(crop[1]+crop[3])/2]]

print 'points_mark:',points_mark

targets=[] # get targets field
for point in points_mark:
	for i in xrange(0,len(crops_demark)):
		for crop in crops_demark[i]:
			if crop[0] < point[0] < crop[2] and crop[1] < point[1] < crop[3]:
				targets += [crop]

print 'targets:',
pprint(targets)
filter_marked_words(demark_denoise,targets).save("targets_filterd.jpg","JPEG")
draw_rectangle2(origin,targets).save("targets.jpg","JPEG")

targets_truncate = get_crops_truncate(targets,demark_denoise) # issue: targets was changed
print 'targets_truncate:',
pprint(targets_truncate)
filter_marked_words(demark_denoise,targets_truncate).save("targets_filterd_cut.jpg","JPEG")
list_marked_words(demark_denoise,targets_truncate,line_height).save("targets_list_cut.jpg","JPEG")

# idntify each
words = []
for target in targets_truncate:
	block = demark_denoise.crop((target[0],target[1],target[2],target[3]))
	#print 'result:',tesserocr.image_to_text(block)	
	word=[tesserocr.image_to_text(block)]
	words+=word

print 'words:',
pprint(words)





