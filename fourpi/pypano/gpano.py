import json
import subprocess
from config import OpenPanoConfigurationMaker

EXIFTOOL = "exiftool"

def dummy(image):
    #pipe = subprocess.Popen(EXIFTOOL + " " + image, shell=True, stderr=subprocess.PIPE)
    #output = pipe.stderr.read()
    exif = subprocess.check_output([EXIFTOOL, '-j', image])
    return json.loads(exif)[0]



if __name__ == '__main__':

    #exif = dummy('/home/reimer/Bilder/Panoramen/schaukel.jpg')
    exif = dummy('/home/reimer/Bilder/Panoramen/anonymous.jpg')
    for k in exif.keys():
        print k
    direction = exif.get('PoseHeadingDegrees', None)
    pan = exif.get('InitialViewHeadingDegrees', None)
    tilt = exif.get('InitialViewPitchDegrees',None)
    fov = exif.get('InitialHorizontalFOVDegrees', None)
    
    conf = OpenPanoConfigurationMaker(debug=True)
    conf.add_panorama('laschozas', 'pano/laschozas_f.xml', pan=pan, tilt=tilt, fov=fov, direction=direction)
    print conf.get_conf()

    
    