#!/usr/bin/env python

import tile

pano = tile.Panorama('/home/reimer/tmp/dzi/laschozas.jpg')

#for w in range(2000,2002,1):
for w in [15080]:
    f,t = pano._get_cubesize(w)
    print "# %d, %d, %d" % (w,f,t)