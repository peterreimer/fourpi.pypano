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

class OpenPanoConfigurationMaker:

    def __init__(self, config_file=None, debug=False):
        """bla"""
        if config_file:
            tree = ET.ElementTree(file=config_file)
            salado = tree.getroot()
        else:
            salado = ET.Element("SaladoPlayer")
            panoramas = ET.SubElement(salado, "panoramas")
            glob = ET.SubElement(salado, "global")
            modules = ET.SubElement(salado, "modules")
            
        glob = salado.find('global')
        glob.set('debug', str(debug).lower()) 
        if not debug:
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

    def _make_location(self, pan, tilt, distance):
        
        location = []
        if pan:
            location.append('pan:%.1f' % pan)
        if tilt:
            location.append('tilt:%.1f' % tilt)
        if distance:
            location.append('distance:%.1f' % distance)
        return ','.join(location)

   
    def add_hotspot(self, pano_id, hotspot_id, path, pan, target):
        """add hotspots"""
        salado = self.salado
        parent = salado.find('panoramas')
        panoramas = parent.findall('panorama')
        for panorama in panoramas:
            if panorama.get('id') == pano_id:
                hotspot_attributes = {}
                hotspot_attributes['id'] = hotspot_id 
                hotspot_attributes['path'] = path
                hotspot_attributes['target'] = target
                hotspot_attributes['location'] = self._make_location(pan, 0, 400) 
                image =  ET.SubElement(panorama, "image", attrib=hotspot_attributes)


    def add_panorama(self, pano_id, path, direction="0", **kwargs):
        """sfd"""
        salado = self.salado
        pan = kwargs.get('pan', 0.0)
        tilt = kwargs.get('tilt', 0.0)
        fov = kwargs.get('fov', 100)
        pano_attributes = {}
        pano_attributes['id'] = pano_id  
        pano_attributes['path'] = path 
        pano_attributes['direction'] = str(direction) 
        view = self._make_view(pan, tilt, fov)
        if view:
            pano_attributes['view'] = view 
        panoramas = salado.find('panoramas')
        panorama =  ET.SubElement(panoramas, "panorama", attrib=pano_attributes)
        
        self.salado = salado


    def get_conf(self):
        salado = self.salado
        indent(salado)
        return ET.tostring(salado, encoding='utf-8')

if __name__ == '__main__':

    conf = OpenPanoConfigurationMaker('salado.xml', debug=True)
    #conf = OpenPanoConfigurationMaker()
    conf.add_panorama('zeughaus', 'pano/zeughaus_f.xml')
    conf.add_panorama('dummy', 'pano/dummy_f.xml')
    conf.add_panorama('laschozas', 'pano/laschozas_f.xml', pan=123.4, tilt=15)
    for pano_id in ('zeughaus','laschozas','dummy'):
        for target_id in ('zeughaus','laschozas','dummy'):
            if target_id is not pano_id:
                hotspot_id = '%s-%s' % (pano_id, target_id)
                path = "~tours/checker/_media/images/spots/arrow_blue.png"
                conf.add_hotspot(pano_id, hotspot_id, path, 45, target_id)

    print conf.get_conf()
