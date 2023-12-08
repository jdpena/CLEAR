# XXX A. XXX. Distribution is unlimited.

# XXX supported XXXnder XXX of XXX for 
# XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
# findings, XXX 
# of the author(s) XXX the XXX 
# XXX of XXX for XXX and XXX.

# © 2023 XXX.

# XXX.XXX-11 Patent Rights - XXX (May 2014)

# The software/XXX-Is basis

# XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
# XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
# XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
# XXX XXX.S. XXX may violate any copyrights that exist in this work.

from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)
from Drones.GeneralSupport.GeneralDroneServer import DroneServer as DS

# Need to move spot specific things into this class.
# Takeout of the generic which currently houses it 
class DroneServer(DS):
    def __init__(self, interfaceUrl, drone) -> None:
        self.interfaceAddress = interfaceUrl
        super().__init__(self.interfaceAddress, drone)
        self.grabReady = False

    #Can be spurred by either roboclick or user click being vouched.
    #Means there will be a grab command sent to the drone
    def userClickUpdated(self, message):
        #If waiting for roboclicked to be vouched for
        # being at this function means it was vouced for

        url = "{}/click".format(self.URL)
        response = self.session.get(url, verify=False)
        data = response.json()
        print("The data for user click is {}".format(data))
        click = data["click"]

        point = (click['x'], click['y'])

        if response.status_code == self.GOOD_CODE:
            self.sendInstructions("grab{}".format(point))
        else :
            print("Failed to get click: status code", response.status_code)

    def considerUserClick(self, message):
        # This click was proposed by a web user
        url = "{}/considerClick".format(self.URL)
        self.drone.movementController.completedAction()

        response = self.session.get(url, verify=False)
        data = response.json()
        print("The data for user click is {}".format(data))
        click = data["click"]
        point = (click['x'], click['y'])
        self.drone.grabObject(userTarget = point)