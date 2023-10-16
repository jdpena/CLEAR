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

import subprocess, os
import requests, time
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

class ServerHandler():
    def __init__(self, url, name, checker):
        self.session = requests.Session()
        self.session.verify = False
        self.ADDRESS = url
        self.name = name
        print(url)
        self.checker = checker

    def requestReadiness(self):
        try:
            self.session.post(f"{self.ADDRESS}/readyreset", verify=False)
            time.sleep(2)

            self.session.post(f"{self.ADDRESS}/readyrequest", verify=False)
            self.checker.services[self.name]['active'] = True
        except Exception as e:
            self.checker.services[self.name]['active'] = False
            print(f"The {self.name} server is not operational")

    def checkConnection(self):
        try:
            url = f"{self.ADDRESS}/readyInfo"
            response = self.session.get(url, verify=False)
            self.checkForReady(response.content)
            self.checker.services[self.name]['active'] = True
        except Exception as e:
            self.checker.services[self.name]['active'] = False
            print(f"The {self.name} server is not operational")

    def checkForReady(self, message):
        message = str(message)
        print(message)
        for key, _ in self.checker.services.items():
            if key in message:
                target = f"{key} is "
                index = message.find(target) + len(target)

                ERROR_SIGNAL = "NOT"
                if message[index:index + len(ERROR_SIGNAL)] != ERROR_SIGNAL:
                    self.checker.services[key]['active'] = True
                else:
                    self.checker.services[key]['active'] = False
