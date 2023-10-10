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

import requests, json, time
from Platform import ChatPlatform

class GPTOnlineOffNetwork(ChatPlatform):
    def __init__(self, baseDir, url):
        super().__init__(baseDir, url)
        self.url = "https://autodrone.azurewebsites.net/chat"
        self.modelName = "gpt-4"
        self.waitingTime = 20
        self.timeLastCalled = 0
        self.scriptStartTime = time.time()

    def getResponse(self, messages, timesTried = 0):
        if self.timeLastCalled + self.waitingTime > time.time() :
            time.sleep((self.timeLastCalled + self.waitingTime) - time.time())
            print("waiting ", self.waitingTime)
        
        
        self.timeLastCalled = time.time()

        if timesTried >= 3 : 
                print("bummers")
                return "Too many tokens"
        try :
            # posts and gets reply at the same time.
            response = requests.post(self.url, json={'string': messages, 'model' : self.modelName}, timeout = self.waitingTime * 2)

            print (response.content)

            return (self.extract_message(response.content) if response.status_code == 200 
                else self.getResponse(messages, timesTried=timesTried+1))
        except Exception as e :
            time.sleep(2)
            return self.getResponse(messages, timesTried=timesTried+1)
    
    #process input for codes or commands
    def givenInput(self, messages, code = None):
        if code is not None :
            if "gpt-3.5" in code :
                self.modelName = "gpt-3.5-turbo"
                self.waitingTime = 1

            elif "gpt-4" in code :
                self.modelName = "gpt-4"
                self.waitingTime = 20

            self.giveName()
            return "mess(command heard)"
           
        # if self.hasHourPassed() :
        #     if self.modelName == "gpt-3.5-turbo":
        #         self.modelName = "gpt-4"
        #         self.waitingTime = 5
        #     else:
        #         self.modelName = "gpt-3.5-turbo"
        #         self.waitingTime = 1
        #     print("hello")
            
        #     self.giveName()
        #     print("\n \n \n swithced \n \n\n")
        #     return "mess(command heard)"

        return self.getResponse(messages)

    def extract_message(self, response_content):
        # Parse the response content as JSON
        decoded_content = response_content.decode('utf-8')
        content_json = json.loads(decoded_content)

        # Extract the 'message' field
        message = content_json.get('message', '')

        print ("The message is : ", message)
        return message

    def giveName(self, message=None) :
        print("my name is, ", self.modelName)
        url = '{}/llmModel'.format(self.URL)
        response = requests.post(url, json={'model': self.modelName})
        print("model name requested : ", response)

    #Returns True if an hour or more has passed since the script started, False otherwise.
    def hasHourPassed(self):
        hourHasPassed = (time.time() - self.scriptStartTime) >= 30
        if hourHasPassed:
            self.scriptStartTime = time.time()
        return hourHasPassed