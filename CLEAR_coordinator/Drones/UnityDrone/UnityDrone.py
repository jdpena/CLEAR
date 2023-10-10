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

from Drones.UnityDrone.DroneServer import DroneServer
from MovementControllers.AerialController.AerialController import MovementController
from Drones.GeneralSupport.GeneralDrone import GeneralDrone
import copy

class UnityDrone(GeneralDrone) :
    def __init__(self, interfaceUrl) ->None:
        self.server = DroneServer(interfaceUrl, self)
        super().__init__()

        self.GPT_SET_UP = "Drones/UnityDrone/llmInfo/gptCharacter"
        self.GPT_EVOLUTION = "Drones/UnityDrone/llmInfo/gptProgress"
        self.FPS = 30
        self.FOV = 60
        self.NAME = "UnityDrone"
        self.isAerial = True
        self.specificActions = [{"restart" : self.restart}, 
                                {"throw" : self.throwObject}]
        
        self.UNINTERRUPTIBLE_ACTIONS = []
        self.queryIfOperating = self.queryIfFlying

        self.PROPORTIONAL_GAIN = 0.01
        self.INTEGRAL_GAIN = 0.0
        self.DERIVATIVE_GAIN = 0.02

        self.TOO_CLOSE_TARGET_DISTANCE = 1.2
        self.TOO_CLOSE_GENERAL_DISTANCE = 1.15
        self.SLOW_DOWN_RANGE = 1.8

        self.movementController = MovementController(self)

        self.NEEDS_HUMAN_APPROVAL = False

    #Grab object is called by the llm
    #it will simulate a user click for the web client
    def throwObject(self, target = None, userTarget = None) : 
        if target is not None :
            point = copy.deepcopy(target.midpoint)
        elif userTarget is not None :
            point = userTarget
        else : raise("Function either needs a target or a point")
        
        if (self.checkIfCommandOccuring() or 
          self.server.waitingForClickResponse): 
            return 
        
        # If it does not need to be vetted, it will just throw.
        if not self.NEEDS_HUMAN_APPROVAL:
            self.server.sendInstructions("throw{}".format(point))
            return 

        self.startingStateChange()

        print("throwing at {}".format(point))
        self.server.postClick(point)
    
    def restart(self, foo = None) :
        self.server.sendInstructions("restart")
        self.movementController.completedAction()
    
    def sendMovementControls(self, left_right_velocity, for_back_velocity,
     vertical_velocity, yaw_velocity) :
        
        if (self.checkIfCommandOccuring() or 
          self.server.waitingForClickResponse): 
            return 
        
        input = [for_back_velocity, left_right_velocity, 
                 vertical_velocity, yaw_velocity]
        
        self.server.sendMovement(input)

    def queryIfFlying(self, askForText = False) :
        if askForText :
            return "You are flying and can move"
        return True