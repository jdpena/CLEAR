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
class Target():
    def __init__(self, screenDimension, depth):
        self.active = False
        self.screenWidth = screenDimension
        self.target = None
        self.depth = depth
        # self.lock = threading.Lock()

    def updateScreenDimensions(self, screenWidth):
        self.screenWidth = screenWidth

    #Sets the target to no longer be considered
    #active. This then stops tracking processes
    def setUnactive(self) :
        self.active = False

    #Sets the perceieved distance between the drone
    #and the target. To clarify, does not tell
    #movement to maintain this distance, but instead
    #just notes the current distance between the drone and 
    #the object. 
    def setDistance(self, distance) :
        self.distance = distance
    
    #Sets the target to be a certain object, updating the 
    #the target, alongside the object which was 
    #selected to be the target. 
    def setTarget(self, target, depth) :
        self.target = target
        self.midpoint = self.target.midpoint
        self.target.isTarget = True
        self.distance = self.depth.getElement((self.midpoint[1],self.midpoint[0]))

        self.target.timeUpdated = time.time()
        self.active = True
        text = self.target.generalObjectName

        print("target set to ".format(str(text)))

    # def getTarget(self) :
    #     self.lock.acquire(blocking=True)

    #     self.commandLock.release()

    #updates the lastfound position of the target.
    def updateTarget(self, midpoint) :
        self.midpoint = midpoint 
        self.distance = self.depth.getElement((self.midpoint[1],self.midpoint[0]))

    
    #checks if the target midpoint x position is within 
    #10% of the midpoint of the screen. 
    def facingTheTarget(self, threshold = .10) :
        midwidthImg = self.screenWidth/2
        dif = self.target.midpoint[0] - midwidthImg
        if abs(dif/midwidthImg) < threshold :
            return True
        return False
    