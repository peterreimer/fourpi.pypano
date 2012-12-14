#!/usr/bin/env  python
import extract

faces = (
    (   0,  0,0,90, "f"), #front
    (  90,  0,0,90, "l"), #left
    ( -90,  0,0,90, "r"), #right
    (-180,  0,0,90, "b"), #back
    (   0,-90,0,90, "u"), #up
    (   0, 90,0,90, "d")  #down
)
views = []
for yaw, pitch, roll, fov, pos in faces:
    views.append(extract.View(yaw, pitch, roll, fov))

pano_file = open("pano.jpg","rb")
pano = extract.Extractor(pano_file,views=views)
pano.extract()

for view in pano.views:
    print view.image.size
