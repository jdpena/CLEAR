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

"""
This class platforms communication from drone back to the controller
"""
class FeedbackHandler() :
    def __init__(self, drone) -> None:
        self.drone = drone
        self.PostURL =  "{}/feedbackInfo".format(self.drone.URL)

    def giveFeedback(self, question) :
        try :
            if question == "state?" : 
                data = {"commandOccuring" : self.drone.performingCommand, "grabReady" : self.drone.controller.arm.readyToGrab}
                response = self.drone.session.post(self.PostURL, json={"feedback":data},verify=False)
                        
        except Exception as e : 
            with open("feedbackError.txt", "w") as file:
                    file.write("The error is : {}".format(e))
    
    def giveComment(self, comment):
        data = {"comment" : comment}
        response = self.drone.session.post(self.PostURL, json={"feedback":data},verify=False)




    
