# DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

# This material is based upon work supported by the Under Secretary of Defense for 
# Research and Engineering under Air Force Contract No. FA8702-15-D-0001. Any opinions,
# findings, conclusions or recommendations expressed in this material are those 
# of the author(s) and do not necessarily reflect the views of the Under 
# Secretary of Defense for Research and Engineering.

# © 2023 Massachusetts Institute of Technology.

# Subject to FAR52.227-11 Patent Rights - Ownership by the contractor (May 2014)

# The software/firmware is provided to you on an As-Is basis

# Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 
# 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. Government rights in this work are defined by DFARS 252.227-7013 or 
# DFARS 252.227-7014 as detailed above. Use of this work other than as specifically
# authorized by the U.S. Government may violate any copyrights that exist in this work.

import argparse, os
from Drones.UnityDrone.UnityDrone import UnityDrone
from Drones.Spot.SpotDrone import SpotDrone
from DroneController import DroneController

"""
This script launches the application, determines 
the system being utilized, and spins off  
threads pertaining to system action, and system 
connectivity
"""

if __name__ == '__main__':
    # Create a mapping between drone names and their respective classes
    droneMapping = {
          "UnityDrone": UnityDrone,
          "SpotDrone": SpotDrone
    }

    parser = argparse.ArgumentParser()

     # Check for environment variable for worker address, if not found use default
    defaultWorkerAddress = os.environ.get('WORKER_ADDRESS', "http://localhost:9090")

    defaultInterfaceAddress = os.environ.get('INTERFACE_ADDRESS', "https://localhost:7070")

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
    
    parser.add_argument('--run_perpetually', 
      type=bool, default=True)
    
    args = parser.parse_args()

    # Sets the parent class
    platform = droneMapping[args.platform]
    workerAddress = args.worker_address
    interfaceAddress = args.interface_address
    showDroneView = args.drone_view
    manualControlOnly = args.manual_control
    perpetualRun = args.run_perpetually

    print(("The worker server address is {}\n"
          +"The interface server address is {}").
          format(workerAddress,interfaceAddress))
    
    systemRuns = 0

    while True:
        try:
          #instantiates the drone, waits for connections to be approved
          DroneController(platform)(workerAddress, 
                        interfaceAddress, manualControlOnly)
          systemRuns += 1
        except Exception as e:
           print(f"The Error is {e}")