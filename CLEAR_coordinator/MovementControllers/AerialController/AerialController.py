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

from MovementControllers.GeneralMovementController import MovementController as GMC

class MovementController(GMC) :
    def __init__(self, drone) -> None:
        super().__init__(drone)

        for i in drone.specificActions :
            drone.actionDict.update(i)

        self.drone.currentRotation = None
        self.IFly = True
        self.queryIfOperating = self.drone.queryIfFlying

    def run(self) :
        self.droneMovement()