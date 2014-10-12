fourpi.pypano
=============

Some helper scripts for creating spherical panoramas. The stitching program nona of 
the [Hugin project](http://hugin.sourceforge.net) is required to do the actual work


gpano2openpano
--------------

read the https://developers.google.com/photo-sphere/metadata/?hl=de from a panorama and create the xml configuration file for the openpano/saladao viewer


|GPano:UsePanoramaViewer | |
|GPano:CaptureSoftware | |
|GPano:StitchingSoftware | |
|GPano:ProjectionType | |
|GPano:PoseHeadingDegrees | direction|
|GPano:PosePitchDegrees | |
|GPano:PoseRollDegrees | |
|GPano:InitialViewHeadingDegrees | view:pan |
|GPano:InitialViewPitchDegrees | view:tilt |
|GPano:InitialViewRollDegrees | |
|GPano:InitialHorizontalFOVDegrees | view:fov |
|GPano:FirstPhotoDate | |
|GPano:LastPhotoDate | |
|GPano:SourcePhotosCount | |
|GPano:ExposureLockUsed | |
|GPano:CroppedAreaImageWidthPixels | |
|GPano:CroppedAreaImageHeightPixels | |
|GPano:FullPanoWidthPixels | |
|GPano:FullPanoHeightPixels | |
|GPano:CroppedAreaLeftPixels | |
|GPano:CroppedAreaTopPixels | |

 https://developers.google.com/photo-sphere/metadata/?hl=de
