# CLEAR_interface_server
The CLEAR interface server integrates human input into the CLEAR system, and also connects the CLEAR coordinator with the robot. The interface server offers a web UI that hosts conversations between users and the robot. This UI supports a two-way messaging service, a view of the robot’s vision, a robot action approval system, and a means for the user to control the robot manually. This screen can be accessed at ``https://<hostname>:7070/views/controller.html``. The interface server also offers API services that connect the robot to the coordinator.
 
Run the interface server on a Windows or Unix-based systems with Node.js 18
Installed. Also, perform the following commands:
``openssl genpkey -algorithm RSA -out key.pem``
``openssl req -new -x509 -key key.pem -out cert.pem -days 365``
 
Following this, place the resulting files into the security directory.
 
To run the service, use
``node serverSecure.js``

-----

XXX A. XXX. Distribution is unlimited.
 
XXX supported XXXnder XXX of XXX for XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions, findings, conclusions or recommendations XXX(s) XXX the XXX XXX of XXX for XXX and XXX.

© 2023 XXX.

XXX.XXX-11 Patent Rights - XXX (May 2014)

The software/XXX-Is basis

SPDX-License-Identifier: XXX
