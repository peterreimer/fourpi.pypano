#!/usr/bin/env   python
import os
from xml.etree.ElementTree import ElementTree, SubElement
import logging
from optparse import OptionParser

logger = logging.getLogger('pano')
hdlr = logging.FileHandler('pano.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

EXP = "Exposure"
ufrawrc = os.path.expanduser("~/.ufrawrc")
logger.info("reading %s" % (ufrawrc))
tree = ElementTree()
tree.parse(ufrawrc)
ufraw = tree.getroot()
print ufraw.tag
exposure = tree.find(EXP)
if exposure is not None:
    ev = float(exposure.text)
else:
    ev = 0.0
    exposure = SubElement(ufraw, EXP)


print ev
e=1
for n in [4, 5]:
    exp_range = (float(n) - 1) * e
    lowest = ev - exp_range / 2
    exposures = []
    for i in range(n):
         exposures.append(round(lowest + i * e, 2))
    print exposures

for exp in exposures:
    c = "ufraw%+.2f.xml" % exp
    exposure.text = str(exp)
    tree.write(c)

