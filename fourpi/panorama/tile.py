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
DEFAULT_TILESIZE = 512
MINIMUM_TILESIZE = 400
MAXIMUM_TILESIZE = 600
SCRIPT = """p f0 w%(size)s h%(size)s v%(fov)s u10  n"PNG"\n
i f4 w%(width)s h%(height)s y%(yaw)s p%(pitch)s r%(roll)s v%(hfov)s n"%(input)s" """

class Panorama:
    
    def __init__(self, src, hfov=360):
        
        self.image =  PIL.Image.open(src)
        self.src = src
        self.filename = os.path.split(self.src)[1]
        self.hfov = hfov
        self.width, self.height = self.image.size
        self.cubesize, self.tilesize = self._get_cubesize(self.width)

    def _get_default_facewidth(self, opt):
        print opt
        level = 0
        while 2**level < opt:
            level = level + 1
            facesize = 2**(level-1)
            if facesize <= DEFAULT_TILESIZE:
                tilesize = facesize
        print facesize, tilesize
        return facesize, tilesize
                
    def _get_cubesize(self, panowidth):
        rawcubesize = panowidth / math.pi
        zoomlevels = int(rawcubesize / MINIMUM_TILESIZE) + 1
        divider = 2**zoomlevels
        tilenumber = (rawcubesize - rawcubesize % divider) / divider
        optcubesize = tilenumber * divider
        tilesize = 0
        scaling = 1
        logger.info("opt cube %s" % (optcubesize))
        # calculate all possible tile sizes
        for zoomlevel in range(zoomlevels):
            tilewidth = optcubesize / 2**zoomlevel
            #print zoomlevel, facesize, tilewidth
            if MINIMUM_TILESIZE <= tilewidth and tilewidth <= MAXIMUM_TILESIZE:
                tilesize = tilewidth
                facesize = optcubesize
        if tilesize == 0:
            facesize, tilesize = self._get_default_facewidth(optcubesize)

        scaling = facesize / float(rawcubesize)
        logger.info("Scaling down %s" % (scaling))
        logger.info("Cube / tile size %s/%s" % (facesize,tilesize))
        return facesize, tilesize
    
    def _make_script(self, yaw, pitch, roll, fov):
        
        tmp_fd, tmp_name = tempfile.mkstemp(".txt", STITCHER)           
        
        #size, tile = self._get_size(self.width, fov)
        
        input_parameter = {
            'input':_expand(self.src),
            'width':self.width,
            'height':self.height,
            'yaw':yaw,
            'pitch':pitch,
            'roll':roll,
            'fov':fov,
            'hfov':self.hfov,
            'size': self.cubesize 
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
            creator = ImageCreator(tile_size=self.tilesize)
            creator.create(face, dest)
            logger.info("Created Pyramid for %s" % face)
            os.rename(dest, xml)
            os.rename(base + "_files", base) # TODO: check if dest folder exist
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
    
