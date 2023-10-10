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

import subprocess, os

def printInstructions(choosingAction) :
    print ("The actions you may choose are : ")
    for i in choosingAction :
        print (i)
    print("pair an action with a service")

def setRobot() :
    print("Setting the robot platform")
    service = input("provide the name of robot applicaiton you want to run :\n")

    PATH_TO_FILE="ProjectBuilder/settingRobot.sh"

    if service not in os.environ:
        robotClassName = input("provide the class of the robot defined in the coordinator :\n")
        robotRunInstructions = input("provide a command that launches the application from its root directory :\n")
        gitUrl = input("provide the git URL for {} :\n".format(service))
        
        # This restarts the setup application
        subprocess.run(['./{}'.format(PATH_TO_FILE), service, robotClassName, 
                    robotRunInstructions, gitUrl])
    
    # This restarts the setup application
    subprocess.run(['./{}'.format(PATH_TO_FILE), service])

    exit(0)

def queryUser(launch, choosingAction, shouldPrint = False):
    # os.system('clear')

    if shouldPrint : printInstructions(choosingAction)

    print("Choose an action to perform. For instructions enter '?'")

    num_to_service = {}
    service_names = set()
    i = 1
    for message in launch.getReadiness():
        print(f"{i} : {message}")
        service_name = message.split(" ")[0]  # Extract the service name from the message
        num_to_service[i] = service_name  # Map the index to the service name
        service_names.add(service_name)
        i += 1

    userInput = input().strip().split(" ")

    if userInput[0] == '?' :
        return queryUser(launch, choosingAction, shouldPrint=True)
    elif userInput[0] == "-1" :
        return False    
    elif len(userInput) != 2:
        print("Invalid input format.")
        return True

    action, identifier = userInput[0], userInput[1]

    # The user had indicated they want to perform 
    # an action for all services
    if identifier.lower() == "all" :
        try :
            for service in service_names :
                choosingAction[action](service)
        except Exception as e :
            print (e)
    elif action in choosingAction:
        if identifier.isdigit() and int(identifier) in num_to_service:
            choosingAction[action](num_to_service[int(identifier)])  # Call the action with the appropriate service
        elif identifier in service_names:
            choosingAction[action](identifier)  # Call the action with the provided service name
        else:
            print("Invalid number or service name.")
    else:
        print("Invalid action.")

    return True
