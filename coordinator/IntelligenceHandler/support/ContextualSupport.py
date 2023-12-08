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

import time, re

"""
ContextualSupport is used for for generating contextual information
applied to feeding the LLM worker. It houses varius useful functions.
"""
class ContextualSupport() :
    def __init__(self, ) -> None:
        self.timeOfLaunch = time.time()
        self.SECONDS_PER_MINUTE = 60

        # Used for cleaning LLM responses
        # Personal note: Needs to be updated for modularity. Use specific actions dict and general
        # This is crud [>:(]
        self.paramActionsExpectingString = ["sequence", "mess", "rotate"]
        self.paramActionsExpectingID = ["moveto", "throw", "lookat"]
        self.actionsWithoutParam = ["restart", "stop", "no"]
        ####################################

    #Used to generate background details such as system state, and
    #time elapsed
    def generateBackgroundContext(self, target = None) :
        context = self.getRunDuration()
        if target != None : 
            targetDescription = "focused on object {}".format(target.tag)
            context = "{}\n {}".format(context,targetDescription)
        return context

    #Sees how long the system has been running for.
    def getRunDuration(self) :
        currentTime = time.time()
        timeRunning = int(currentTime - self.timeOfLaunch)

        minutesElapsed = self.secondsIntoMinutes(timeRunning)

        strOutput = "Time elapsed since launch : "

        if minutesElapsed > 0 :
            strOutput += "{} minutes ".format(minutesElapsed)
        
        strOutput += "{} seconds".format(timeRunning%self.SECONDS_PER_MINUTE)

        return strOutput

    def secondsIntoMinutes(self, secondsPassed) :
        return int(secondsPassed/self.SECONDS_PER_MINUTE)
    
    #Seperates sequence into several notes that will be applied
    #to following LLM worker calls 
    def separateSequence(self, inputString):
        # remove opening and closing parentheses
        cleanString = inputString.strip('()')
        cleanString = str(cleanString).replace("sequence", "")
        
        # split the string by commas and strip leading/trailing white space
        stringList = [x.strip() for x in cleanString.split(',')]
        
        return stringList
    
    def processLlmResponse(self, response):
        actionOptions = (self.paramActionsExpectingString 
            + self.paramActionsExpectingID + self.actionsWithoutParam)
        # Search for any action in the string

        action_positions = {action: response.lower().find(action) for action in actionOptions if action in response.lower()}
        if action_positions:
            desiredAction = min(action_positions, key=action_positions.get)
        else:
            desiredAction = response
        
        # Moves the response to where the desired action ends
        response = response[str(response).find(desiredAction) + len(desiredAction):]
        
        cleanedResponse = desiredAction
        if desiredAction in self.paramActionsExpectingID:
            objectId = findFirstDigitString(response)
            print("objectID is ", objectId)
            cleanedResponse = f"{desiredAction}({objectId})"

        elif desiredAction in self.paramActionsExpectingString:
            message = getMessage(response)
            # Conditions allows for actions that are supposed to have 
            # messages, but also can tolerates without: Rotate
            if message is not None:
                cleanedResponse = f"{desiredAction}({message})"

        print("The cleaned response is: ", cleanedResponse)
        return cleanedResponse

def findFirstDigitString(inputString):
    # Regular expression pattern for finding digits
    pattern = r'\d+'

    # Search for the pattern in the input string
    match = re.search(pattern, inputString)

    if match:
        return match.group()
    else:
        return None

def getMessage(inputString):
    startIndex = inputString.find('(')
    endIndex = -1
    openCount = 0

    if startIndex != -1:
        for i in range(startIndex, len(inputString)):
            if inputString[i] == '(':
                openCount += 1
            elif inputString[i] == ')':
                openCount -= 1
                if openCount == 0:
                    endIndex = i
                    break

        if endIndex != -1:
            return inputString[startIndex+1:endIndex]
        else:
            # Return None or handle the case for unmatched '('
            return None

    return None

