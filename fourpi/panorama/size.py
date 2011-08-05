#!/usr/bin/env python
import math
#import PIL.Image

#image =  PIL.Image.open('pano6000.jpg')
#width, height = image.size

minimumTileSize = 400
maximumTileSize = 600

notile = []

def get_max_facewidth(zoomlevels, opt):
    
    liste = {}
    for zoomlevel in range(zoomlevels):
        minfacewidth = minimumTileSize * 2**zoomlevel
        if minfacewidth < opt:
            diff = abs(minfacewidth - opt)
            liste[diff] = (minfacewidth, minimumTileSize)
        maxfacewidth = maximumTileSize * 2**zoomlevel
        if maxfacewidth < opt:
            diff = abs(maxfacewidth - opt)
            liste[diff] = (maxfacewidth, maximumTileSize)
    
    return liste[min(liste.keys())]

for hfov in range(3000, 10000, 1):
#for hfov in range(3819, 3822, 1):
    opt = hfov / math.pi
    zoomlevels = int(opt / minimumTileSize) + 1
    #zoomlevels = 5 
    divider = 2**zoomlevels
    #print zoomlevels
    #print divider
    tilenumber = (opt - opt % divider) / divider
    optfacesize = tilenumber * divider
    tilesize = 0
    scaling = 1
    # calculate all possible tile sizes
    for zoomlevel in range(zoomlevels):
        tilewidth = optfacesize / 2**zoomlevel
        #print zoomlevel, facesize, tilewidth
        if minimumTileSize <= tilewidth and tilewidth <= maximumTileSize:
            tilesize = tilewidth
            facesize = optfacesize
            marker = " "
    if tilesize == 0:
        notile.append(hfov)
        marker = "*"
        facesize, tilesize = get_max_facewidth(zoomlevels, opt)
        scaling = facesize / float(optfacesize)
    print "%d %f %d %d %f" % (hfov, opt, facesize, tilesize, scaling)
    
