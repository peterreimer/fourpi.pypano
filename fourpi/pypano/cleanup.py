#!/usr/bin/env   python
import os
import shutil
from operator import itemgetter
import xml.dom.minidom
"""
wrong_atribute = "xmlns"
dzxml = '/home/peter/tmp/dzi/opera/opera_l.xml'
docxml = xml.dom.minidom.parse(dzxml)
image = docxml.getElementsByTagName("Image")[0]
if image.hasAttribute(wrong_atribute):
    image.removeAttribute(wrong_atribute)
docxml.writexml(open(dzxml,"w"))
"""


pyr = "/home/peter/tmp/dzi/lissabon/lissabon_d"

levels = {}
for root, dirs, files in os.walk(pyr):
    if root is not pyr:
        level = int(os.path.split(root)[-1])
        levels[level] = len(files) 
print len(levels)
for level in range(len(levels) - 1):
    level_dir = "/".join((pyr,str(level))) 
    if not levels[level + 1] > 1 and os.path.isdir(level_dir):
        shutil.rmtree(level_dir)
        print "delete " + level_dir
        
    
