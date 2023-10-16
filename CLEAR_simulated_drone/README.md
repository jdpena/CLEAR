# CLEAR_virtual_drone
The CLEAR virtual drone service is a CLEAR robot implementation directly interfaces with a simulated quadcopter in Unity. The virtual drone service controls the robot according to the coordinator's instructions. The virtual drone service receives various commands from the coordinator, such as velocities, throw, and reset position.
 
Run the CLEAR virtual drone service on a Windows or Unix system. Install Unity and then create a project. Once a scene is ready, import the virtual drone into your project. Additionally, ensure that the address file in launch is in a higher directory from the virtual drone. Further, ensure that the value in address matches the address of the interface server.
 
With Unity, you may either run it from the editor or build the project and then run the build.


It should be noted that since our default object detection model (YOLO v8) is trained on real-world objects, simulated assets in the scene where the quadcopter is placed should be sufficiently realistic that the model would recognize them. Attempts to use the quadcopter in more stylized scenes have shown poor recognition performance.

-----

XXX A. XXX. Distribution is unlimited.
 
XXX supported XXXnder XXX of XXX for XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions, findings, conclusions or recommendations XXX(s) XXX the XXX XXX of XXX for XXX and XXX.

© 2023 XXX.

XXX.XXX-11 Patent Rights - XXX (May 2014)

The software/XXX-Is basis

SPDX-License-Identifier: XXX
