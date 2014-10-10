#!/usr/bin/env python
"""tile - A Python script to produce cubic faces and tiles from panos """

__version__ = (0, 0, 1)
__author__ = "Peter Reimer <peter@4pi.org>"


import PIL.Image
import tempfile
import os
import math
import subprocess
import shutil
import logging
import xml.dom.minidom
import argparse

from deepzoom import ImageCreator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

PI = math.pi
STITCHER = "nona"
DEFAULT_TILESIZE = 512
MINIMUM_TILESIZE = 400
MAXIMUM_TILESIZE = 600
DEFAULT_QUALITY = 0.8
SCRIPT = """p f0 w%(size)s h%(size)s v%(fov)s u10  n"PNG"\n
i f4 w%(width)s h%(height)s y%(yaw)s p%(pitch)s r%(roll)s v%(hfov)s n"%(input)s" """

class Panorama:

    def __init__(self, src, quality=DEFAULT_QUALITY, hfov=360):
        self.image = PIL.Image.open(src)
        self.src = src
        self.filename = os.path.split(self.src)[1]
        self.hfov = hfov
        self.quality = quality
        self.width, self.height = self.image.size
        logger.info("size: %d x %d " % (self.width, self.height))
        self.cubesize, self.tilesize = self._get_cubesize(self.width)

    def _get_default_facewidth(self, optcubesize):
        """ calculate a default cubic face and tile size based on exponents of 2
            if we can not find one between MINIMUM_TILESIZE and MAXIMUM_TILESIZE
        """
         
        level = 0
        while 2**level < optcubesize:
            level = level + 1
            facesize = 2**(level-1)
            if facesize <= DEFAULT_TILESIZE:
                tilesize = facesize
        return facesize, tilesize

    def _get_cubesize(self, panowidth):
        rawcubesize = panowidth / math.pi
        zoomlevels = int(rawcubesize / MINIMUM_TILESIZE) + 1
        divider = 2**zoomlevels
        tilenumber = (rawcubesize - rawcubesize % divider) / divider
        optcubesize = tilenumber * divider
        tilesize = 0
        scaling = 1
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
        logger.info("Cube %s | tile %s | scaling %s" % (facesize, tilesize, scaling))
        return facesize, tilesize

    def _make_script(self, yaw, pitch, roll, fov):
        """create a temporary projectfile for the stitcher"""
        
        tmp_fd, tmp_name = tempfile.mkstemp(".txt", STITCHER)           
        
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
        
        script = os.fdopen(tmp_fd, "w")
        script.writelines(SCRIPT % input_parameter)
        return tmp_name

    def extract(self, yaw, pitch, roll, fov, dest, name):
        """extract a cubic face from the panorama"""

        if not dest:
            dest = _expand(os.path.dirname(self.src))
        outfile = os.path.join(dest,name)
        
        script = self._make_script(yaw, pitch, roll, fov)
        args = (STITCHER, '-o', outfile, script)
        nona = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        nona.communicate()
        logger.info(script)
        os.remove(script)
        
        result = _expand(outfile + '.png')
        logger.info(outfile)
        
        if os.path.isfile(result):
            return result
        else:
            return None
                
    def _make_cubic(self):
        """ extract the six faces of a cube
        """

        faces = (
            (0, 0, 0, 90, "f"),    # front
            (90, 0, 0, 90, "l"),   # left
            (-90, 0, 0, 90, "r"),  # right
            (-180, 0, 0, 90, "b"), # back
            (0, -90, 0, 90, "u"),  # up
            (0, 90, 0, 90, "d")    # down
        )
         
        dest = _get_or_create_path(os.path.splitext(self.src)[0])
        facefiles = []
        for yaw, pitch, roll, fov, pos in faces:
            name = '_'.join((os.path.splitext(self.filename)[0], pos))
            face = self.extract(yaw, pitch, roll, fov, dest, name)
            facefiles.append(face)
                         
        return facefiles

    def salado(self):
        faces = self._make_cubic()
        
        pyramids = []
        for face in faces:
            base = os.path.splitext(face)[0]
            dest = base + ".dzi"
            xml = base + ".xml"
            tilesdir = base + "_files"
            creator = ImageCreator(tile_size=self.tilesize, tile_format="jpg",
                                   image_quality=self.quality, resize_filter=None)
            creator.create(face, dest, discard_levels=True)
            msg = "Created Pyramid for %s" % face
            print msg
            #logger.info(msg)
            if base.endswith('_f'):
                os.rename(dest, xml)
                self.fix_xml(xml)
            else:
                os.remove(dest)
            if os.path.isdir(base):
                shutil.rmtree(base)
            os.rename(tilesdir, base)
            pyramids.append(base)
            os.remove(face)

    def fix_xml(self, dzxml):
        wrong_atribute = "xmlns"
        #dzxml = '/home/peter/tmp/dzi/opera/opera_l.xml'
        docxml = xml.dom.minidom.parse(dzxml)
        image = docxml.getElementsByTagName("Image")[0]
        if image.hasAttribute(wrong_atribute):
            image.removeAttribute(wrong_atribute)
            docxml.writexml(open(dzxml, "w"))


def _expand(d):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(d)))

def _get_or_create_path(path):
    """create a directory if it does not exist."""

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

    parser = argparse.ArgumentParser(description='Convert equirectangular panorama to six pyramids')
    parser.add_argument('panorama', help='Panoramic image')
    parser.add_argument("-q", "--quality", default=DEFAULT_QUALITY, type=float, help="JPG compression level, default is %s" % DEFAULT_QUALITY)
    parser.add_argument("-v", "--verbose", action="store_true", help="be verbose")

    args = parser.parse_args()
    print args    
    pano = Panorama(args.panorama, quality=args.quality)
    pano.salado()
    
    
