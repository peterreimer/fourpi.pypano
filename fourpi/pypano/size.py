#!/usr/bin/env python
import logging
import tile

logger = logging.getLogger('pano')
hdlr = logging.FileHandler('pano.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


pano = tile.Panorama('/home/reimer/tmp/dzi/laschozas.jpg')

#for w in range(2000,2002,1):
for w in [15080]:
    f,t = pano._get_cubesize(w)
    print "# %d, %d, %d" % (w,f,t)