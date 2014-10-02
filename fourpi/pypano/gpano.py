#!/usr/bin/env  python
import json
import os
import subprocess
from config import OpenPanoConfigurationMaker
#from fourpi.pypano.size import pano

EXIFTOOL = "exiftool"

def get_exif(image):
    #pipe = subprocess.Popen(EXIFTOOL + " " + image, shell=True, stderr=subprocess.PIPE)
    #output = pipe.stderr.read()
    if os.path.isfile(image):
        exif = subprocess.check_output([EXIFTOOL, '-j', image])
        return json.loads(exif)[0]
    else:
        return None


if __name__ == '__main__':

    conf = OpenPanoConfigurationMaker(debug=True)

    #exif = dummy('/home/reimer/Bilder/Panoramen/schaukel.jpg')
    panos = ('/home/reimer/Bilder/Panoramen/anonymous.jpg',
             '/home/reimer/Bilder/Panoramen/markt-eq.jpg'  )
    for pano in panos:
        if os.path.isfile(pano):
            filename = os.path.basename(pano)
            shortname, extension = os.path.splitext(filename)
            exif = get_exif(pano)
            direction = exif.get('PoseHeadingDegrees', None)
            pan = exif.get('InitialViewHeadingDegrees', None)
            tilt = exif.get('InitialViewPitchDegrees',None)
            fov = exif.get('InitialHorizontalFOVDegrees', None)
        
            conf.add_panorama(shortname, '%s/%s_f.xml' % (shortname, shortname), pan=pan, tilt=tilt, fov=fov, direction=direction)
    print conf.get_conf()

    
    
