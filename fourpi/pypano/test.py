#!/usr/bin/env  python
import PIL.Image
import extract

image = PIL.Image.open("pano.jpg")
pano = extract.Extractor(image,views=[])
print pano.get_extracted_views()
print pano.save()