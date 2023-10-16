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
    if shouldPrint : printInstructions(choosingAction)

    print("Choose an action to perform. For instructions enter '?'")

    num_to_service = {}
    service_names = set()
    i = 1
    for message in launch.getReadiness():
        print(f"{i} : {message}")
        # Extract the service name from the message
        service_name = message.split(" ")[0] 

        # Map the index to the service name 
        num_to_service[i] = service_name 

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
