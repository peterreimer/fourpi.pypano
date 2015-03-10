#!/usr/bin/env  python

from __future__ import unicode_literals, print_function
import json
import logging
import math
from distutils.spawn import find_executable

logger = logging.getLogger(__name__)

EXIFTOOL = find_executable('exiftool')

if EXIFTOOL:
    print("exiftool found at %s" % EXIFTOOL)
else:
    logger.error("EXIFTOOL required but not found.")

class Scene():
    def __init__(self, title):
        self.conf = {}
        self.conf['title'] =  title

class Tour():
    
    def __init__(self, firstScene=None, author=None, panoramas=[]):
        self.conf = {}
        default = {}
        scenes = {}
        if author:
            default['author'] = author
        default['firstScene'] = firstScene
        self.conf['default'] = default
        self.conf['scenes'] = scenes
        
        for panorama in panoramas:
            print(panorama)

    def _add_scene(self, scene_id, title, yaw=0, pitch=0):
        """add multires panorama to tour"""
        conf = {}
        conf['title'] = title
        conf['yaw'] = yaw
        conf['pitch'] = pitch
        conf['type'] = 'multires'
        conf['multires'] = {}
        conf['hotSpots'] = []
        self.conf['scenes'][scene_id] = conf
        return

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
        return json.dumps(self.conf)


if __name__ == '__main__':
    panos = [
        '/home/reimer/Development/4pi.org/content/tiles/gehry-bauten/gehry-bauten.jpg'
    ]
    tour = Tour("dummy", "Peter Reimer", panoramas=panos)
    #tour._add_scene('laschozas', 'Mirador las Chozas')    
    #tour.add_hotspot('laschozas', 'ziel', 'Ziel')    
    #tour.add_hotspot('laschozas', 'ziel2', 'Ziel Zwei')    
    print(tour.get_json())
