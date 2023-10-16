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