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

"""
launches edge device for controlling spot
"""
from Interface.Interface import Interface
import argparse, os

parser = argparse.ArgumentParser()

defaultWorkerAddress = os.environ.get('WORKER_ADDRESS',
                                  "https://localhost:7070")

parser.add_argument('--serverAddress', type=str,
  default=defaultWorkerAddress)

# Wifi ip
parser.add_argument('--spotAddress', type=str,
  default="wifi")

serverURL = parser.parse_args().serverAddress
spotURL = parser.parse_args().spotAddress

if str(spotURL).lower == "lan" :
     spotURL = os.environ.get('SPOT_LAN_ADDRESS')
elif str(spotURL).lower == "wifi" :
     spotURL = os.environ.get('SPOT_WIFI_ADDRESS')

print(spotURL)

if __name__ == '__main__':
    robot = Interface(serverAddress = serverURL,
      spotAddress = spotURL)
