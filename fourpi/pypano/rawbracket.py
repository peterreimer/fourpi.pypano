#!/usr/bin/env   python
import os
import xml.dom.minidom
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
ufrawxml = xml.dom.minidom.parse(ufrawrc)
exposure = ufrawxml.getElementsByTagName(EXP)[0]
ev = float(exposure.firstChild.data)
exposure.firstChild.data = float(ev) + 0.5
ufrawxml.writexml(open("ufraw-2.xml","w"))


print ev
e=1
for n in [4, 5]:
    exp_range = (float(n) - 1) * e
    lowest = ev - exp_range / 2
    exposures = []
    for i in range(n):
         exposures.append(round(lowest + i * e, 2))
    print exposures
