#!/usr/bin/env python
from PIL import Image
#import PIL.Image

RATIO = (4, 1)
SCALE = 1.66
PREVIEW_WIDTH = 600


im = Image.open("hummelwiese.jpg")
#im = Image.open("dartmoor.jpg")

w, h = im.size
print w, h
ratio = float(w) / float(h)
if ratio < float(RATIO[0]) / float(RATIO[1]):
    print "crop!"

im.thumbnail((PREVIEW_WIDTH, PREVIEW_WIDTH), Image.NEAREST)

im.save('preview.jpg', "JPEG", quality=85)

w, h = im.size
height = w / RATIO[0] 
offset = int(0.5 * (h - w / RATIO[0]))
# (left, upper, right, lower) 
box = (0, offset ,w , offset + height)
area = im.crop(box)

area.save('cropped.jpg', "JPEG", quality=85)