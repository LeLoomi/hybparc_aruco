Hybparc Aruco
==============

Hands on ECG-placement Training software for med students.

-> To have the software save the annotated pictures, create a 'results' directory. (Care, per pass 1 pic meaning rn per analysis 10-15 pictures, uncompressed!)

General requirements
--------------------

> We recommend running this software in its own environment, e.g. conda
- OpenCV
- Numpy
- PyQt6
- [ArucoRoi](https://GitHub.com/LeLoomi/ArucoRoi) <small>(Must be manually put in /lib/)<sup>1</sup></small>
- qt-material <small>(for styling only, but has to be manually removed from the code if unwanted)</small>

<small>1: Correct the import error in detector.py by changing `import services` to `from . import services`.</small>

Linux specific adjustments
--------------------------

<u>Video capture id:</u><br>
Windows and MacOS use id 0 for the first camera, 1 for the second and so on. On Linux a USB camera has multiple `dev/videoX` interfaces, e.g. `video0` to `video3` for the first and `video4` to `video7` for the second camera. We recommend using the lowest interface per camera, i.e. 0 and 4. Using the Win/Mac 0 and 1 indices will result in an attempt to grab from the same camera, crashing the software.

<u>Video capture resolution and format:</u><br>
On Linux OpenCV (/the V4L2 driver) defaults to something, which is likely the lowest resolution and a wrong/limiting capture format. This can be fixed by setting the cv capture properties by hand, e.g. if our camera supports 3840x2160 via MJPG, the following should be applied to <u>all</u> your VideoCapture objects:
```` Python
stream.set(cv.CV_CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        stream.set(cv.CV_CAP_PROP_FRAME_WIDTH, 3840)
        stream.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 2160)
````
To check available capture indices/devices run `v4l2-ctl --list-devices`
To check available formats, resolutions run `v4l2-ctl -d /dev/videoX --list-formats-ext`

<u>OpenCV and Python version:</u><br>
On MacOS and Windows PyQt6 supports Python 3.12. On Linux however, only Python 3.9 is currently<sup>Dec '24</sup> supported. You will have to downgrade your environment to Python 3.9 or you will be unable to install PyQt6.
<br>Additionally, potential issues may arise from which OpenCV package you install. On MacOS the standard opencv-python package works well. On Linux not everything might be supported. In case of crashes we recommend opencv-contrib-python.
