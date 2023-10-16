# CLEAR_coordinator

The CLEAR coordinator serves as the system middleman, collecting, analyzing, and sending data between the interface and worker server while dictating robot behavior. One such process occurs with handling image data: images are captured by the drone and then sent to the interface server; from here, it is provided to the coordinator, which then shares it with the worker server. The computer vision services then turns this visual data into contextual information. Following this, the computer vision gives the worker server this context, which the coordinator collects. The coordinator then uses this context to create a robotic response command, which is then shared with the interface server and redistributed to the robot for execution. Further, the coordinator controls the robot through a layer of abstraction, yielding high-level robot instructions regarding movement and specific commands that will be interpreted by the services directly attached to the robot.
 
Run CLEAR coordinator on a Windows or Unix system in a Python 3.8 interpreter accompanied by the packages expressed in setup/requirements.txt. To run the service, use
 
``python main.py --worker_address <web address> --interface_address < web address > --platform <UnityDrone||SpotDrone>``
 
Alternatively, you can run the script through the CLEAR_setup services.
 
Also, do ensure you run this system only after starting the interface server, worker server, and llm chat services.
 
-----

XXX A. XXX. Distribution is unlimited.
 
XXX supported XXXnder XXX of XXX for XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions, findings, conclusions or recommendations XXX(s) XXX the XXX XXX of XXX for XXX and XXX.

© 2023 XXX.

XXX.XXX-11 Patent Rights - XXX (May 2014)

The software/XXX-Is basis

SPDX-License-Identifier: XXX
