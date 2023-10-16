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

"""
ContextualSupport is used for for generating contextual information
applied to feeding the LLM worker. It houses varius useful functions.
"""
class ContextualSupport() :
    def __init__(self) -> None:
        self.timeOfLaunch = time.time()
        self.SECONDS_PER_MINUTE = 60

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
    def separateSequence(self, input_string):
        # remove opening and closing parentheses
        clean_string = input_string.strip('()')
        clean_string = str(clean_string).replace("sequence", "")
        
        # split the string by commas and strip leading/trailing white space
        string_list = [x.strip() for x in clean_string.split(',')]
        
        return string_list
