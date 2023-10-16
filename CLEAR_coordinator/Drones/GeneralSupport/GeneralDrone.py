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

import time

class GeneralDrone() :
    def __init__(self) ->None:
        self.imageParts = {}
        self.waitingForImage = True
        self.image = None
        self.rotation = None
        self.image = self.getImage()
        self.getRotation()
        self.speed = 1
    
    #Checks if busy. If busy will return true
    #but also it will ask if actually busy.
    def checkIfCommandOccuring(self) : 
        if not self.server.commandOccuring :
            return False
        
        self.getState()
        return True

    def startingStateChange(self) :
        self.movementController.stopMovement(True)
        self.sendMovementControls(0,0,0,0)
        DELAY = 1
        time.sleep(DELAY)

    def getState(self, foo = None) :
        self.server.sendInstructions("state?")

    # should make it just call for image to be sent 
    def getImage(self):
        self.image = self.server.getImage()
        return self.image

    def getRotation(self) :
        rawRotation = self.server.getRotation()
        if rawRotation == None : 
            self.currentYawRotation = self.currentRotation = 0
        else :
            self.currentRotation = stringToInArray(self.server.getRotation())
            self.currentYawRotation = self.currentRotation[1]
        return self.currentRotation
    
def stringToInArray(s):
    parts = s.split(',')
    ints = [float(part) for part in parts]
    return ints
