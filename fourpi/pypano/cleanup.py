#!/usr/bin/env   python
import os
import xml.dom.minidom
wrong_atribute = "xmlns"
dzxml = '/home/peter/tmp/dzi/opera/opera_l.xml'
docxml = xml.dom.minidom.parse(dzxml)
image = docxml.getElementsByTagName("Image")[0]
if image.hasAttribute(wrong_atribute):
    image.removeAttribute(wrong_atribute)
docxml.writexml(open(dzxml,"w"))