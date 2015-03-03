#!/usr/bin/env  python

from __future__ import unicode_literals, print_function
import json

class Scene():
    def __init__(self, title):
        self.conf = {}
        self.conf['title'] =  title

class Tour():
    
    def __init__(self, firstScene, author):
        self.conf = {}
        default = {}
        scenes = {}
        default['author'] = author
        default['firstScene'] = firstScene
        self.conf['default'] = default
        self.conf['scenes'] = scenes

    def add_scene(self, scene_id, title):
        """add multires panorama to tour"""
        #scene = Scene()
        conf = {}
        conf['title'] = title
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
    
    tour = Tour("dummy", "Peter Reimer")
    tour.add_scene('laschozas', 'Mirador las Chozas')    
    tour.add_hotspot('laschozas', 'ziel', 'Ziel')    
    tour.add_hotspot('laschozas', 'ziel2', 'Ziel Zwei')    
    print(tour.get_json())
