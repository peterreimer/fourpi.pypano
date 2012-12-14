#/usr/bin/env   python
from PIL import Image
import tempfile
import os
import math
import subprocess

PI = math.pi
STITCHER = "nona"
SCRIPT = """p f0 w%(size)s h%(size)s v%(fov)s u10  n"PNG"\n
i f4 w%(width)s h%(height)s y%(yaw)s p%(pitch)s r%(roll)s v%(hfov)s n"%(input)s" """

class View:
    
    def __init__(self, yaw, pitch, roll, fov, width=None, height=None):
        
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.fov = fov
        self.width = width
        self.height = height

class Extractor:
    
    def __init__(self, panorama_file, views=[], hfov=360):

        self.panorama_file = panorama_file
        self.panorama = Image.open(panorama_file)
        self.hfov = hfov
        self.width, self.height = self.panorama.size
        self.views = views

    def get_extracted_views(self):
        return len(self.views)

    def _save_pano(self):
        """store the panorama temporarily on disk"""
        #extension = "." + self.panorama.format
        extension = ".jpg"
        tmp_fd, panorama_filename = tempfile.mkstemp(suffix=extension)                                                       
        self.panorama.save(panorama_filename, quality=95)
        return panorama_filename
    
    def extract(self):
        infile = self._save_pano()
        for view in self.views:
            script = self._make_script(infile, view.yaw, view.pitch, view.roll, view.fov)
            tmp_fd, outfile = tempfile.mkstemp(".png",STITCHER)                                                       
            args = (STITCHER,'-o', outfile, script)
            nona = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            nona.communicate()
            view.image = Image.open(outfile)
            os.remove(outfile)
            os.remove(script)
        self._del_pano(infile)

    def _del_pano(self, panorama):
        os.remove(panorama)
        
    def _make_script(self, infile, yaw, pitch, roll, fov):
        
        tmp_fd, script_name = tempfile.mkstemp(".txt", STITCHER)           
        
        input_parameter = {
            'input':infile,
            'width':self.width,
            'height':self.height,
            'yaw':yaw,
            'pitch':pitch,
            'roll':roll,
            'fov':fov,
            'hfov':self.hfov,
            'size': 1000
            }
        
        script = os.fdopen(tmp_fd,"w")
        script.writelines(SCRIPT % input_parameter)
        print "Create script at %s" % script_name
        return script_name
    
