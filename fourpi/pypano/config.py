#!/usr/bin/env  python
import elementtree.ElementTree as ET

def indent(elem, level=0):
    """pretty printing of xml formats """

    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class Panorama:

    def __init__(self, id, direction=0, **kwargs):
        pano =  ET.Element("panorama")


class OpenPanoConfigurationMaker:

    def __init__(self, debug=False):
        """bla"""
    
        sp =  ET.Element("SaladoPlayer")

        glob = ET.SubElement(sp, "global", debug=str(debug))
        panoramas = ET.SubElement(sp, "panoramas")
        modules = ET.SubElement(sp, "modules")
        actions= ET.SubElement(sp, "actions")

        self.xml = sp

    def add_panorama(self, id, path, direction=0, **kwargs):
        """sfd"""
        pan = kwargs.get('pan', 0)
        tilt = kwargs.get('tilt', 0)
        fov = kwargs.get('fov', 100)
        
        #pano =  ET.Element("panorama", id=id, path=path, direction=direction)
        print self.xml.get('panoramas')

    def get_conf(self):
        xml = self.xml
        indent(xml)
        return ET.tostring(xml, encoding='utf-8')

if __name__ == '__main__':

    conf = OpenPanoConfigurationMaker(debug=True)
    conf.add_panorama('zeughaus', 'pano/zeughaus_f.xml')
    print conf.get_conf()
