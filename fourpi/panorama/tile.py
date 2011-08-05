#!/usr/bin/env python
"""tile - A Python script to produce cubic faces and tiles from panos """

__version__ = (0, 0, 1)
__author__ = "Peter Reimer <peter@4pi.org>"


import PIL.Image
import tempfile
import os
import math
import subprocess
import logging
from optparse import OptionParser
from deepzoom import ImageCreator

logger = logging.getLogger('pano')
hdlr = logging.FileHandler('pano.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

PI = math.pi
STITCHER = "nona"
MINIMUM_TILE_SIZE = 400
MAXIMUM_TILE_SIZE = 600
SCRIPT = """p f0 w%(size)s h%(size)s v%(fov)s u10  n"PNG"\n
i f4 w%(width)s h%(height)s y%(yaw)s p%(pitch)s r%(roll)s v%(hfov)s n"%(input)s" """

class Panorama:
    
    def __init__(self, src, hfov=360):
        
        self.image =  PIL.Image.open(src)
        self.src = src
        self.filename = os.path.split(self.src)[1]
        self.hfov = hfov
        self.width, self.height = self.image.size

    def get_max_facewidth(self, zoomlevels, opt):
        
        liste = {}
        for zoomlevel in range(zoomlevels):
            minfacewidth = MINIMUM_TILE_SIZE * 2**zoomlevel
            if minfacewidth < opt:
                diff = abs(minfacewidth - opt)
                liste[diff] = (minfacewidth, MINIMUM_TILE_SIZE)
            maxfacewidth = MAXIMUM_TILE_SIZE * 2**zoomlevel
            if maxfacewidth < opt:
                diff = abs(maxfacewidth - opt)
                liste[diff] = (maxfacewidth, MAXIMUM_TILE_SIZE)
    
        return liste[min(liste.keys())]
    
    def _get_size(self, hfov, fov):
        opt = hfov / math.pi
        zoomlevels = int(opt / MINIMUM_TILE_SIZE) + 1
        divider = 2**zoomlevels
        tilenumber = (opt - opt % divider) / divider
        optfacesize = tilenumber * divider
        tilesize = 0
        scaling = 1
        # calculate all possible tile sizes
        for zoomlevel in range(zoomlevels):
            tilewidth = optfacesize / 2**zoomlevel
            #print zoomlevel, facesize, tilewidth
            if MINIMUM_TILE_SIZE <= tilewidth and tilewidth <= MAXIMUM_TILE_SIZE:
                tilesize = tilewidth
                facesize = optfacesize
        if tilesize == 0:
            facesize, tilesize = self.get_max_facewidth(zoomlevels, opt)
            scaling = facesize / float(optfacesize)
        return facesize, tilesize
    
    def _make_script(self, yaw, pitch, roll, fov):
        
        tmp_fd, tmp_name = tempfile.mkstemp(".txt", STITCHER)           
        
        #size, tile = self._get_size(self.hfov, fov)
        size = 512
        input_parameter = {
            'input':_expand(self.src),
            'width':self.width,
            'height':self.height,
            'yaw':yaw,
            'pitch':pitch,
            'roll':roll,
            'fov':fov,
            'hfov':self.hfov,
            'size': size 
            }
        
        script = os.fdopen(tmp_fd,"w")
        script.writelines(SCRIPT % input_parameter)
        # logger.info("Create script at %s" % tmp_name)
        return tmp_name
        
    def extract(self, yaw, pitch, roll, fov, dest, name):
        
        if not dest:
            dest = _expand(os.path.dirname(self.src))
        
        
        outfile = os.path.join(dest,name)
        script = self._make_script(yaw, pitch, roll, fov)
        args = (STITCHER,'-o', outfile, script)
        nona = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        nona.communicate()
        os.remove(script)
        # logger.info("Remove script %s" % script)
        result = _expand(outfile + '.png')
        
        if os.path.isfile(result):
            return result
        else:
            return None
        
        
        
                
    def _make_cubic(self):
        
        faces = (
            (   0,  0,0,90, "f"), #front
            (  90,  0,0,90, "l"), #left
            ( -90,  0,0,90, "r"), #right
            (-180,  0,0,90, "b"), #back
            (   0,-90,0,90, "u"), #up
            (   0, 90,0,90, "d")  #down
        )
         
        dest = _get_or_create_path(os.path.splitext(self.src)[0])
        facefiles = []
        for yaw, pitch, roll, fov, pos in faces:
            name = '_'.join((os.path.splitext(self.filename)[0], pos))
            face = self.extract(yaw, pitch, roll, fov, dest, name)
            logger.info("Extract face %s" % name)
            facefiles.append(face)
                         
        return facefiles

    def salado(self):
        faces = self._make_cubic()
        
        for face in faces:
            base = os.path.splitext(face)[0]
            dest = base + ".dzi"
            xml = base + ".xml"
            creator = ImageCreator()
            creator.create(face, dest)
            logger.info("Created Pyramid for %s" % face)
            os.rename(dest, xml)
            os.rename(base + "_files", base)
            os.remove(face)
            
            


def _expand(d):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(d)))

def _get_or_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

 
def whereis(program):
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and \
           not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None
        
def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="read data from FILENAME")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    if options.verbose:
        print "reading %s..." % options.filename

    
    pano = Panorama(args[0])
    #pano.extract(0, -25, -15, 75, None, 'zenit')
    #pano._make_cubic()
    pano.salado()
    
    

if __name__ == "__main__":
    main()
    
