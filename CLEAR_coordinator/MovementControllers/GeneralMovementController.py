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

import copy, time
from MovementControllers.PID import PIDController

#This class is a parent class for all dynamic drone movement controllers.
#All drones which have basic movement employ this class. Generic actions are 
#defined here such as moveto, lookat, rotate, stop. These are movement commands
#all drones have the ability to use. However, actions that are also defined in 
#for specifc drones will be called from here. It is
#responsible for triggering the process of sending movement commands to the drone,
#defining basic actions for the drone, and handling all other movement commands.
class MovementController() :
    def __init__(self,drone) -> None:
        self.drone = drone
        self.left_right_velocity = self.for_back_velocity = self.vertical_velocity = self.yaw_velocity = 0
        self.drone.actionDict = {"moveto" : self.autoPursue, 
                                 "lookat" : self.lookat, 
                                 "rotate" : self.rotateInPlace,
                                 "stop" : self.resetDrone}
        
        self.pid_controller = PIDController(kp=self.drone.PROPORTIONAL_GAIN,
                                             ki=self.drone.INTEGRAL_GAIN, 
                                             kd=self.drone.DERIVATIVE_GAIN)
        self.actionFunction = None

        #Used for gauging target velocity. 
        self.previous_midpoint = (0,0)
        self.SPEED = 1

    #droneMovement is the main loop for movement. If there is manual
    #control commands being sent, then the drone will respond accordingly to
    #that. These controls come from user input on the interface web-app, like with 
    #WASD and such. If there are no manual controls being sent, and there are controls
    #being produced internally by the automation, then use these controls. 
    #Each interation will assign the velocities with a value. If the when checking to stop movement
    #if the there is any velocity which does not equal zero, then should stop will be set to True. 
    #If shouldStop = True, then in following iterations where stopMovement is called, if 
    #all velocities are zero, then then an all zero velocity will be sent to the drone.
    #This practice prevents needless movement commands to be sent. For example, 
    #an all zero movement command send will only need to occur once, it will not be continually sent. 
    def droneMovement (self) :
        shouldStop = False
        try:
            while self.drone.intelligence.droneIsRunning:
                # refers to yaw rotation
                self.drone.getRotation()

                if self.manualControl() or self.autoControl():
                    self.drone.sendMovementControls(self.left_right_velocity, 
                    self.for_back_velocity, self.vertical_velocity,
                    self.yaw_velocity)
                        
                shouldStop = self.stopMovement(shouldStop)
                time.sleep(10/self.drone.FPS)
        except Exception as e: 
            print("movement error : {}".format(e))

            # self.drone.intelligence.droneIsRunning = False

    #If significant keys are pressed, then movement will 
    #occur. 
    def manualControl(self):
        change = False
        arr = copy.deepcopy(self.drone.server.keysPressed)

        if 'r' in arr:  # set forward velocity
            self.vertical_velocity = self.SPEED
            change = True
        elif 'f' in arr:  # set backward velocity
            self.vertical_velocity = -self.SPEED
            change = True
        if 'a' in arr:  # set left velocity
            self.left_right_velocity = -self.SPEED
            change = True
        elif 'd' in arr:  # set right velocity
            self.left_right_velocity = self.SPEED
            change = True
        if 'w' in arr:  # set up velocity
            self.for_back_velocity = self.SPEED
            change = True
        elif 's' in arr:  # set down velocity
            self.for_back_velocity = -self.SPEED
            change = True
        if 'q' in arr:  # set yaw counter clockwise velocity
            self.yaw_velocity = -self.SPEED
            change = True
        elif 'e' in arr:  # set yaw clockwise velocity
            self.yaw_velocity = self.SPEED
            change = True
        
        if 'escape' in arr:
            self.drone.intelligence.droneIsRunning = False

        if hasattr(self.drone, "manualControls") :
            action = self.drone.manualControls()
            if action is not None :
                self.drone.intelligence.action = action

        return change

    #Checks if sending all zero movement should occur. if it should
    # then sends all zero movement to the drone. Otherwise just continues to 
    # assign velocity to zero
    def stopMovement(self, shouldStop) :
        if  (not self.left_right_velocity 
             and not self.for_back_velocity 
             and not self.vertical_velocity 
             and not self.yaw_velocity):
            
            if shouldStop :
                self.drone.sendMovementControls(0,0,0,0)
                print("stop")
            return False
        self.left_right_velocity = 0
        self.for_back_velocity = 0
        self.vertical_velocity = 0
        self.yaw_velocity = 0
        return True
    
    #Sees if given action string matches any keys in the movement dictionary.
    #If there is a match, then the value assigned to the key will be used. 
    def setAction(self, givenActText) :
        if givenActText in self.drone.actionDict :
            self.actionFunction = self.drone.actionDict[givenActText]
            print("performing action : ",givenActText)

    #stops the drone, sending all zero movement, while also reseting the  
    #occuring action. 
    def resetDrone(self, foo = None) :
        self.stopMovement(shouldStop=True)
        self.drone.intelligence.forgetTarget()
        self.completedAction()

    #Rotates the drone to face the target
    def focusedRotate(self, targ) :

        #I am failing to remember why I am using 
        #this target, instead of the deep copied target. 
        #Will test once I am back in Clemson.
        target = self.drone.intelligence.target
        midwidthImg = self.drone.picFrame.shape[0]/2


        if hasattr(target.target, "objectOld") and not target.target.objectOld:
            # Calculate object velocity
            velocity = target.midpoint[0] - self.previous_midpoint[0]
            
            # Predict future position of the object
            predicted_midpoint = target.midpoint[0] + velocity
            
            # Calculate the difference between the predicted position and the center of the image
            dif = predicted_midpoint - midwidthImg

            # basically, just using pixel locations as input 
            value = self.pid_controller.update(dif) 

            if self.drone.intelligence.target.facingTheTarget() :
                value = value/2
                
            self.yaw_velocity = value
        else:
            # quickly turns back to last known rotation of drone
            self.yaw_velocity = 0
            #Was used to try to return to rotation where target was last found. 
            # target.target.lastFoundRotation - self.drone.currentRotation
        print (self.yaw_velocity)
        # Save current position for next iteration
        self.previous_midpoint = target.midpoint

    #Just rotates the drone to the right. 
    #It's simple, and effective for having the robot
    #find additional objects. 
    def rotateInPlace(self, foo) :
        ROTATION_SPEED = self.SPEED/2
        self.yaw_velocity = ROTATION_SPEED
        return True

    #Since not all drones can set elevation, will only
    # be used if the drone has the attribute "isAerial"
    def autoElevate(self, target) :
        # Want the target to be in center focus
        desiredHeight = self.drone.imgHeight/2

        # Get ratio between points. 
        # If the ratio > than 1, move down, else move up
        dif = -((target.midpoint[1]/desiredHeight) - 1.0)

        self.vertical_velocity = self.SPEED * dif

    #This is used when moving to a target. Will move to the target
    #with respect to distance between itself and target, but also
    #in respect to proximity with other objects. If too close to
    #any given thing, will stop pursuing the target.  
    def autoPursue(self, target) :
        self.drone.inPursuit = True
        madeMovement = True
        
        print ("target distance : {}".format(target.distance))
        
        if not target.active :
            self.completedAction()

        multiplier = 1
         
        if (target.target is not None 
            and hasattr(target.target, "objectOld") 
            and target.target.objectOld) :
            multiplier = .5

        # additional slow down functionality
        if hasattr(target.target, "targetTime") :
            madeMovement =  False
        else :
            self.for_back_velocity = (self.SPEED *
                min(abs(target.distance - self.drone.SLOW_DOWN_RANGE), 1) * multiplier)
        
        print("The distance away is: ", self.drone.intelligence.depth.generalDist)

        # just for testing LLM
        self.completedAction()

        if self.drone.TOO_CLOSE_TARGET_DISTANCE > target.distance \
        or self.drone.TOO_CLOSE_GENERAL_DISTANCE > self.drone.intelligence.depth.generalDist:
            print("too close to target!")
            self.completedAction()

        return madeMovement
    
    #As an action, lookout itself does nothing. But, when lookat is 
    #called by the LLM, an object is set to be the target. If there is a target, the robot
    #will rotate to face the target. 
    # there is foo just because how its called
    def lookat(self, foo) :
        self.completedAction()

    #completedAction resets action associated variables 
    #preventing the action from continuing to run. 
    def completedAction(self) :
        self.actionFunction = None
        print ("\n\nintelligent action was : ",  self.drone.intelligence.action)
        self.drone.intelligence.action = ""

    #If the action function has been set, it calls that function.
    #If the action denoted within IntelligenceHandler is set to anything,
    #then the action is set to follow.  
    def considerAction(self, target) :
        #Might change the ordering around. 
        if self.actionFunction != None :
            #preforms current action
            self.actionFunction(target)
        if self.drone.intelligence.action != "" :
            self.setAction(self.drone.intelligence.action)
            return True
        return False

    #autoControl calls and starts all of the autonomous processes.
    #If there is an action that should be performed, it will be called
    #from this funciton. 
    def autoControl(self) :
        targ = copy.deepcopy(self.drone.intelligence.target)
        performedAction = False

        if self.drone.intelligence.action \
            not in self.drone.UNINTERRUPTIBLE_ACTIONS :
                #if target has target time it means its old
                if (targ.active and 
                    not hasattr(targ.target,"targetTime")):
                    self.focusedRotate(targ)

                    if hasattr(self, "IFly") :
                        self.autoElevate(targ)

                    performedAction = True
            
        performedAction += self.considerAction(targ)
        return performedAction
    
    #for automating drone description 
    def describeActions(self, actions) :
        return 