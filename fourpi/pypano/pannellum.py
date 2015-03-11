#!/usr/bin/env  python

from __future__ import unicode_literals, print_function
import subprocess
import json
import logging
import math
import os
from distutils.spawn import find_executable

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
log_string = "%s API %s method: status %s"


EXIFTOOL = find_executable('exiftool')

if EXIFTOOL:
    logger.info("exiftool found at %s" % EXIFTOOL)
else:
    logger.error("EXIFTOOL required but not found.")


class Tour():
    
    def __init__(self, firstScene=None, author=None, panoramas=[]):
        self.conf = {}
        default = {}
        scenes = {}
        if not firstScene and len(panoramas) > 0:
            firstScene = self._scene_id_from_image(panoramas[0])
        if author:
            default['author'] = author
        default['firstScene'] = firstScene
        self.conf['default'] = default
        self.conf['scenes'] = scenes
        
        for panorama in panoramas:
            values = self._get_exif(panorama)
            if values:
                self._add_scene(values['scene_id'], values['scene_id'], yaw=values['pan'], pitch=values['tilt'], northOffset=values['direction'])
            
    def _get_exif(self, image):
        
        scene_id = self._scene_id_from_image(image)
        values = {}
        values['scene_id'] = scene_id
        if os.path.isfile(image):
            exifjson = subprocess.check_output([EXIFTOOL, '-j', '-n', image])
            exif = json.loads(exifjson)[0]
            mapping = (
                 ('direction', 'PoseHeadingDegrees', 0),
                 ('pan', 'InitialViewHeadingDegrees', 0),
                 ('tilt', 'InitialViewPitchDegrees', 0),
                 ('fov', 'InitialHorizontalFOVDegrees', 90),
                 ('lng', 'GPSLongitude', None),
                 ('lat', 'GPSLatitude', None)
            )
            logger.info("Processing image %s" % image)
            for conf, gpano, default in mapping:
                values[conf] = exif.get(gpano,default)             
            return values
        else:
            logger.error("File not found: %s" % image)
            return None

    def _scene_id_from_image(self, image):
        scene_id = os.path.splitext(os.path.basename(image))[0]
        return scene_id

     
    def _add_scene(self, scene_id, title, yaw=0, pitch=0, northOffset=0):
        """add multires panorama to tour"""
        conf = {}
        conf['title'] = title
        conf['yaw'] = yaw
        conf['pitch'] = pitch
        conf['northOffset'] = northOffset
        conf['type'] = 'multires'
        conf['multires'] = self._multires_conf()
        conf['hotSpots'] = []
        self.conf['scenes'][scene_id] = conf
        return
    
    def _multires_conf(self):
        conf = {}
        conf['basePath'] = '../tiles/nideggen/'
        conf['path'] = '%l/%s%y_%x'
        conf['fallbackPath'] =  "fallback/%s"
        conf['extension'] =  "jpg"
        conf['tileResolution'] =  512
        conf['maxLevel'] =  4
        conf['cubeResolution'] = 3816
        return conf

    def add_hotspot(self, scene_id, target_id, text, pitch=0, yaw=0):
        conf = {
            'type': "scene",
            'text': text,
            'sceneId' : target_id,
            'pitch': pitch,
            'yaw':yaw
        }
        self.conf['scenes'][scene_id]['hotSpots'].append(conf)
        return
        
    
    def get_json(self):
        return json.dumps(self.conf, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    panos = [
        '/home/peter/Development/4pi.org/content/tiles/medienhafen-bruecke/medienhafen-bruecke.jpg',
        '/home/peter/Development/4pi.org/content/tiles/gehry-bauten/gehry-bauten.jpg',
        '/home/peter/Development/4pi.org/content/tiles/gehry-bauten/medienhafen2.jpg',
    ]
    tour = Tour(None, "Peter Reimer", panoramas=panos)
    #tour._add_scene('laschozas', 'Mirador las Chozas')    
    #tour.add_hotspot('laschozas', 'ziel', 'Ziel')    
    #tour.add_hotspot('laschozas', 'ziel2', 'Ziel Zwei')    
    print(tour.get_json())
