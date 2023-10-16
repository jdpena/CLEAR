# CLEAR_computer_vision
CLEAR computer vision generates system-understandable perceptual awareness utilized by the coordinator in governing robot response. This software defines two services the CLEAR project uses: CLEAR object detection, and CLEAR depth perception.
 
These services connect to the worker server and listen for image uploads. When a new image is uploaded to the worker server, both of the services retrieve the newly uploaded image from their designated depo. Uploaded images are copied into depth perception and object detection depo. Further, there may exist multiple simultaneously running services of both varieties; for example, a CLEAR project may run two object detection services and three depth perception services. In the case of duplicate services, a First Come First Serve schXXXle will be used.
 
CLEAR object detection transmutes raw visual data into contextual information defined in natural language. This service helps write the prompts provided to the LLM used for controlling the CLEAR system. 
 
Use CLEAR object detection on a UNIX-based system in a Python 3.8 interpreter accompanied by the packages expressed in setup/requirements.txt. Further, download CUDA toolkit 11.4 onto your system: https://developer.nvidia.com/cuda-11-4-0-downloadarchive?target_os=Linux&target_arch=x86_64. To run the service, use
``python main.py --address <address>``
 
CLEAR depth perception transmutes raw visual data into a depth matrix the coordinator uses for basic object avoidance. Use CLEAR depth perception on a UNIX-based system in a Python 3.8 interpreter accompanied by the packages expressed in setup/requirements.txt. To run the service use
``python main.py --address <address> --type dep``
 
Currently defined configuration:
The object detection service employs ultralytics yolov8, https://github.com/ultralytics/ultralytics
 
The depth perception service employs nianticlabs' monodepth2, https://github.com/nianticlabs/monodepth2
 
However, the systems just expressed above can be easily swapped for other similar systems. In the case of changing parts, ensure that the final output provided to the worker server matches the necessary format.

-----

XXX A. XXX. Distribution is unlimited.
 
XXX supported XXXnder XXX of XXX for XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions, findings, conclusions or recommendations XXX(s) XXX the XXX XXX of XXX for XXX and XXX.

© 2023 XXX.

XXX.XXX-11 Patent Rights - XXX (May 2014)

The software/XXX-Is basis

SPDX-License-Identifier: XXX
