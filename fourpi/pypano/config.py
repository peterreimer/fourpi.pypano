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

    def __init__(self, config_file, debug=False):
        """bla"""
        tree = ET.ElementTree(file=config_file)
        salado = tree.getroot()
        
        glob = salado.find('global')
        glob.set('debug', str(debug)) 
        if not debug:
            print "delete ViewFinder"
            modules = salado.find('modules')
            viewfinder = modules.find('ViewFinder')
            if viewfinder:
                modules.remove(viewfinder)
        self.salado = salado

    def _make_view(self, pan, tilt, fov):
        
        view = []
        if pan:
            view.append('pan:%.1f' % pan)
        if tilt:
            view.append('tilt:%.1f' % tilt)
        if fov:
            view.append('fov:%.1f' % fov)
        return ','.join(view)
    
    def add_panorama(self, pano_id, path, direction="0", **kwargs):
        """sfd"""
        salado = self.salado
        pan = kwargs.get('pan', 0)
        tilt = kwargs.get('tilt', 0)
        fov = kwargs.get('fov', 100)
        pano_attributes = {}
        pano_attributes['id'] = pano_id  
        pano_attributes['path'] = path 
        pano_attributes['view'] = self._make_view(pan, tilt, fov)
        panoramas = salado.find('panoramas')
        panorama =  ET.SubElement(panoramas, "panorama", attrib=pano_attributes)
        
        self.salado = salado


    def get_conf(self):
        salado = self.salado
        indent(salado)
        return ET.tostring(salado, encoding='utf-8')

if __name__ == '__main__':


    conf = OpenPanoConfigurationMaker('salado.xml', debug=True)
    conf.add_panorama('zeughaus', 'pano/zeughaus_f.xml')
    conf.add_panorama('laschozas', 'pano/laschozas_f.xml', pan=123.4, tilt=15)
    print conf.get_conf()
