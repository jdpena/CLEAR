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

import threading, argparse, os
from Drones.UnityDrone.UnityDrone import UnityDrone
from Drones.Spot.SpotDrone import SpotDrone
from UserInterface.UserInterface import UserInterface
from IntelligenceHandler.IntelligenceHandler import IntelligenceHandler

"""
This script launches the application, determines 
the system being utilized, and spins off  
threads pertaining to system action, and system 
connectivity
"""

def DroneController(drone):
  class DroneController(drone):
      def __init__(self, workerAddress, interfaceAddress, 
                  manualControlOnly):
          #The web address that handles the worker objects,
          #machines handling object-detection, depth-perception,
          #and LLM inference. 
          self.workerAddress = workerAddress

          #The web address which the drone and human teammates connect to. 
          self.interfaceAddress = interfaceAddress
          self.manualControlOnly = manualControlOnly

          self.movementThread = threading.Thread(target=self.createMovementHandler)
          self.intelThread = threading.Thread(target=self.createIntelligenceHandler)
          
          #instantiate parent object, the specific drone be utilized
          super().__init__(self.interfaceAddress)

          self.picFrame = self.getImage()
          self.imgWidth = self.picFrame.shape[0]
          self.imgHeight = self.picFrame.shape[1]

          self.intelligence = IntelligenceHandler(self, 
            self.workerAddress)

      # Controls system/drone action/movement 
      def createMovementHandler(self) :
        self.movementController.run()
      
      #Used for building an interface for the machine
      #running the controller code
      def createInterfaceHandler(self) :
          UserInterface(self)

      #This handles the worker pool connections:
      #the drone imagery, llm response, etc. 
      #Additionally, houses all of the data asscoiated
      #with the mentioned items. It is integral to 
      #to the system. 
      def createIntelligenceHandler(self) :
          self.intelligence.run()

  return DroneController


if __name__ == '__main__':
    # Create a mapping between drone names and their respective classes
    droneMapping = {
          "UnityDrone": UnityDrone,
          "SpotDrone": SpotDrone
    }

    parser = argparse.ArgumentParser()

     # Check for environment variable for worker address, if not found use default
    defaultWorkerAddress = os.environ.get('WORKER_ADDRESS',
                                          "http://localhost:9090")

    defaultInterfaceAddress = os.environ.get('INTERFACE_ADDRESS', 
                                             "https://localhost:7070")

    parser.add_argument('--worker_address', 
      type=str, default=defaultWorkerAddress)
    
    parser.add_argument('--interface_address', 
      type=str, default=defaultInterfaceAddress)
    
    parser.add_argument('--platform', type=str, 
      required=True, choices=list(droneMapping.keys()))

    parser.add_argument('--drone_view', 
      type=bool, default=False)
    
    parser.add_argument('--manual_control', 
      type=bool, default=False)
    
    args = parser.parse_args()

    # Sets the parent class
    platform = droneMapping[args.platform]
    workerAddress = args.worker_address
    interfaceAddress = args.interface_address
    showDroneView = args.drone_view
    manualControlOnly = args.manual_control

    print(("The worker server address is {}\n"
          +"The interface server address is {}").
          format(workerAddress,interfaceAddress))

    #instantiates the drone, waits for connections to be approved

    drone = DroneController(platform)(workerAddress, 
                  interfaceAddress, manualControlOnly)

    drone.movementThread.start()
    drone.intelThread.start()

    if showDroneView :
      drone.createInterfaceHandler()

    drone.movementThread.join()
    drone.server.resetReadiness()