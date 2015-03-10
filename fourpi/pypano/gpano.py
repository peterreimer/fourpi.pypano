#!/usr/bin/env  python
import json
import os
import subprocess
from configmaker import OpenPanoConfigurationMaker

EXIFTOOL = "exiftool"

def get_exif(image):
    """ Return the EXIF data of an image in json format."""

    if os.path.isfile(image):
        exif = subprocess.check_output([EXIFTOOL, '-j', '-c %.6f', image])
        return json.loads(exif)[0]
    else:
        return None


if __name__ == '__main__':

    conf = OpenPanoConfigurationMaker( debug=True)

    #exif = dummy('/home/reimer/Bilder/Panoramen/schaukel.jpg')
    #panos = ('/home/reimer/Bilder/Panoramen/anonymous.jpg',
    #         '/home/reimer/Bilder/Panoramen/markt-eq.jpg'  )
    panos = ('/home/reimer/Development/4pi.org/content/tiles/medienhafen-hyatt/medienhafen-hyatt.jpg',
              '/home/reimer/Development/4pi.org/content/tiles/gehry-bauten/gehry-bauten.jpg')
    for pano in panos:
        if os.path.isfile(pano):
            filename = os.path.basename(pano)
            shortname, extension = os.path.splitext(filename)
            exif = get_exif(pano)
            print exif
            direction = exif.get('PoseHeadingDegrees', None)
            pan = exif.get('InitialViewHeadingDegrees', None)
            tilt = exif.get('InitialViewPitchDegrees',None)
            fov = exif.get('InitialHorizontalFOVDegrees', None)
            conf.add_panorama(shortname, '%s/%s_f.xml' % (shortname, shortname), pan=pan, tilt=tilt, fov=fov, direction=direction)
        else:
            print "Image %s does not exist" % pano
        

    print conf.get_conf()
    #print conf

    
    
