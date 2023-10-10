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

from Drones.Spot.DroneServer import DroneServer
from MovementControllers.TerrestrialController.TerrestrialController import MovementController
from Drones.GeneralSupport.GeneralDrone import GeneralDrone
import copy

class SpotDrone(GeneralDrone) :
    def __init__(self, interfaceUrl) ->None:
        self.server = DroneServer(interfaceUrl, self)
        super().__init__()
        self.GPT_SET_UP = "Drones/Spot/llmInfo/gptCharacter"
        self.GPT_EVOLUTION = "Drones/Spot/llmInfo/gptProgress"
        self.FPS = 30
        self.FOV = 60
        self.NAME = "Spot"
        self.isStanding = False
        self.specificActions = [{"stand" : self.stand}, 
                                {"sit" : self.sit},
                                {"dock" : self.dock},
                                {"getState" : self.getState},
                                {"grab" : self.grabObject}]
        
        self.TOO_CLOSE_TARGET_DISTANCE = 1.5
        self.TOO_CLOSE_GENERAL_DISTANCE = 1.5
        self.SLOW_DOWN_RANGE = 3
        
        self.queryIfOperating = self.queryIfStanding
        self.PROPORTIONAL_GAIN = 0.05
        self.INTEGRAL_GAIN = 0.00
        self.DERIVATIVE_GAIN = 1
        self.UNINTERRUPTIBLE_ACTIONS = ["dock", "grab"]
        self.movementController = MovementController(self)
    
    def stand(self, foo) :
        if (self.checkIfCommandOccuring() or 
          self.server.waitingForClickResponse): 
            return 
        
        self.startingStateChange()
        self.server.sendInstructions("stand")
        self.movementController.completedAction()
        self.isStanding = True

    def sit(self, foo) :
        if (self.checkIfCommandOccuring() or 
          self.server.waitingForClickResponse): 
            return  

        self.startingStateChange()
        self.server.sendInstructions("sit")
        self.movementController.completedAction()
        self.isStanding = False

    #Grab object is called by the llm
    #it will simulate a user click for the web client
    def grabObject(self, target = None, userTarget = None) :
        if (self.checkIfCommandOccuring() or 
          self.server.waitingForClickResponse): 
            return 
        
        self.startingStateChange()
        if target is not None :
            point = copy.deepcopy(target.midpoint)
        elif userTarget is not None :
            point = userTarget
        else : raise("Function either needs a target or a point")

        print("grabbing at {}".format(point))
        self.server.postClick(point)

    def dock(self, foo = None) :
        if (self.checkIfCommandOccuring() or 
          self.server.waitingForClickResponse): 
            return  

        self.server.sendInstructions("dock")
        self.movementController.completedAction()
    
    def sendMovementControls(self, left_right_velocity, for_back_velocity,
     vertical_velocity, yaw_velocity) :
        
        if (self.checkIfCommandOccuring() or 
          self.server.waitingForClickResponse): 
            return 
        
        input = [left_right_velocity, for_back_velocity,
     for_back_velocity, yaw_velocity]
        print("sending movement")
        self.server.sendMovement(input)

    def queryIfStanding(self, askForText = False) :
        if askForText :
            if self.isStanding :
                return "You are standing and can move"
            return "You are sitting and cannot move"
        
        return self.isStanding
    
    def manualControls(self, arr) :
        if ' ' in arr:
            if self.queryIfOperating() :
                return "sit"
            else:
                return "stand"
        if 'x' in arr:
            return "dock"
        if '0' in arr:
            return "getState"
        return None
        