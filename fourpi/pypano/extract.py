#/usr/bin/env   python
import PIL.Image
import tempfile
import os
import math
import subprocess

PI = math.pi
STITCHER = "nona"
SCRIPT = """p f0 w%(size)s h%(size)s v%(fov)s u10  n"PNG"\n
i f4 w%(width)s h%(height)s y%(yaw)s p%(pitch)s r%(roll)s v%(hfov)s n"%(input)s" """

class View:
    
    def __init__(self, yaw, pitch, roll, fov, width, height):
        
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.fov = fov
        self.width = width
        self.height = height

class Extractor:
    
    def __init__(self, panorama, views, hfov=360):

        self.panorama = panorama
        self.hfov = hfov
        self.width, self.height = self.panorama.size
        self.views = views

    def get_extracted_views(self):
        return self.width

    def save(self):
        """store the panorama temporarily on disk"""
        extension = "." + self.panorama.format
        tmp_fd, panorama_filename = tempfile.mkstemp(suffix=extension)                                                       
        self.panorama.save(tmp_name)
        return panorama_filename