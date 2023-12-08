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

class Builder() :
    def __init__(self) :
        self.services = {
            "CLEAR_worker_server": "https://github.com/XXX-XXX/CLEAR_worker_server.git",
            "CLEAR_interface_server": "https://github.com/XXX-XXX/CLEAR_interface_server.git",
            "CLEAR_computer_vision": "https://github.com/XXX-XXX/CLEAR_computer_vision.git",
            "CLEAR_llm_chat": "https://github.com/XXX-XXX/CLEAR_llm_chat.git",
            "CLEAR_coordinator": "https://github.com/XXX-XXX/CLEAR_coordinator.git"
                        }
        
        # Check if environment variable 'robot' exists
        if 'robot' in os.environ:
            robotName = os.environ["robot"]
            robotGit = os.environ["{}_raw_git".format(robotName)]
            self.services[robotName] = robotGit 

    def buildTheProject(self) :
        try:
            for service, git_url in self.services.items():
                result = subprocess.run(['bash', './ProjectBuilder.sh', service, git_url])
                returnCode = result.returncode
                # If the error code is 6, this means that the setup applicaiton
                # will relaunch in a setup environment
                if returnCode == 6 : exit()
                
        except subprocess.CalledProcessError as e:
            print('The shell script encountered an error:')
            print('Return code:', e.returncode)
            print('Have {} bytes in stderr:\n{}'.format(len(e.stderr), e.stderr.decode()))
        except FileNotFoundError as e:
            print('The shell script was not found:', e)

    def updateApp(self, service) :
        if service in ("CLEAR_object_detection", "CLEAR_depth_perception"):
            service = "CLEAR_computer_vision"

        text = ("Would you like the update via GitHub (yes/no)? \n")
        response = str(input(text)).lower()

        if 'y' in response :
            subprocess.run(['bash', './UpdateApp/UpdateAppFromGit.sh', service])
        else :
            subprocess.run(['bash', './UpdateApp/UpdateAppFromLocal.sh', service])
