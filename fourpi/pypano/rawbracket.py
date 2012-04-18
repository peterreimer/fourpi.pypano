#!/usr/bin/env   python
import os, sys
import subprocess
from xml.etree.ElementTree import ElementTree, SubElement, Element
import logging
from optparse import OptionParser
from utils import get_or_create_path, whereis

logger = logging.getLogger('rawbracket')
hdlr = logging.FileHandler('rawbracket.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

EXP = "Exposure"
UFRAW_BATCH = whereis('ufraw-batch')

ufrawrc = os.path.expanduser("~/.ufrawrc")
logger.info("reading %s" % (ufrawrc))
tree = ElementTree()
tree.parse(ufrawrc)
ufraw = tree.getroot()

exposure = tree.find(EXP)
if exposure is not None:
    ev = float(exposure.text)
else:
    ev = 0.0
    exposure = SubElement(ufraw, EXP)

def get_ufraw_conf(ufrawrc):
    
    logger.info("reading %s" % (ufrawrc))
    conf = ElementTree()
    conf.parse(ufrawrc)
    ufraw = conf.getroot()
    exposure = conf.find(EXP)
    en = conf.find("ExposureNorm")
    if exposure is not None:
        ev = float(exposure.text)
    else:
        ev = 0.0
        #exposure = SubElement(ufraw, EXP)
        exposure = Element(EXP)
        print exposure
        ufraw.insert(3,exposure)
    logger.info("Exposure value found: %f" % ev)
    return conf, ev 

def get_bracket_values(number, difference, exposure):
    
    exp_range = (float(number) - 1) * difference
    lowest = exposure - exp_range / 2
    exposures = []
    for i in range(number):
         exposures.append(round(lowest + i * difference, 2))
    return exposures

def create_bracket_conf(conf, exp):
    exposure = conf.find(EXP)
    conf_filename = "ufraw%+.2f.ufraw" % exp
    logger.info("creating %s" % conf_filename)
    exposure.text = str(exp)
    conf.write(conf_filename)
    return conf_filename 
    
def main():
    
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-n", "--number", dest="number", action="store", type="int", default=3,
                      help="number of exposures")
    
    parser.add_option("-d", "--difference", dest="difference", action="store", type="float", default=1.0,
                      help="difference between exposures")
    
    ufrawrc = os.path.expanduser("~/.ufrawrc")    
    parser.add_option("-c", "--conf", dest="conf", action="store", type="string", default=ufrawrc,
                      help="UFraw configuration file, default is %s" % ufrawrc)
    
    (options, images) = parser.parse_args()
    
    (conf, ev) = get_ufraw_conf(options.conf)
    exposures = get_bracket_values(number=options.number, difference=options.difference, exposure=ev)
    
        
    for exp in exposures:
        conf_filename = create_bracket_conf(conf, exp)
        dir_name = "eb%+.2f" % exp
        ufrawconf = "--conf=%s" % conf_filename 
        path = "--out-path=%s" % get_or_create_path(dir_name)
        
        for image in images:
            args = (UFRAW_BATCH, ufrawconf, path, image)
            develop = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            develop.communicate()

if __name__ == "__main__":
    main()

