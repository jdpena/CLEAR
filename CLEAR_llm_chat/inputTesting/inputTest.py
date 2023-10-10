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

import socketio, requests, base64, threading, json, time

class Test:
    def __init__(self):
        self.sio = socketio.Client()
        # self.URL = 'http://localhost:9090'  # For local testing

        self.URL = 'http://ait-dgx-01:9090'  # For local testing
        # self.URL = "https://autodrone.azurewebsites.net"
        self.wantInstructions = False

        self.pathToProgress = "progress.json"
        self.sio.on("instruction_updated")(self.givenInstruction)

        self.sio.on("client_chat_updated", self.chatInputted)

        videoThread = threading.Thread(target=self.startListen)
        videoThread.start()
        self.sendJson()

    def startListen(self):
        self.sio.connect(self.URL)
    
    def disconnect(self):
        self.sio.disconnect()

    def runningInput(self):
        inputVal = ""
        while inputVal != " ":
            inputVal = input()

            if inputVal == "!" :
                self.requestInstructions()
                continue

            response = requests.post(self.URL+"/hostChatInfo", json={'string': inputVal})
            print(response)

        self.disconnect()

    def chatInputted(self, message):
        print(message)
        response = requests.get(self.URL+"/clientChatInfo")
        print(response)

        if response.status_code == 200:
            print(response.json()['string'])
        else:
            print("Error:", response.status_code, response.text)

    def sendJson(self) :
        data = None
        with open(self.pathToProgress, 'r') as f:
            data = json.load(f)
        url = '{}/instruction'.format(self.URL)
        # Send the POST request
        data.append({"hardware" : "testing"})

        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print("sending instructions response is : {}".format(response))

        if response.status_code == 200:
            print("POST request successful.")
            print("Response:", response.json())
        else:
            print("POST request failed with status code:", response.status_code)

    def requestInstructions(self):
        response = requests.post(self.URL+"/instruction", json={'string': "want"})
        print ("request response {}".format(response))
        self.wantInstructions = True

    def givenInstruction(self, message): 
        if not self.wantInstructions : return

        self.wantInstructions = False

        url = '{}/instruction'.format(self.URL)

        print ("instruction given to me!")
        # Perform GET request to the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Save the JSON object as a file
            with open(self.pathToProgress, "w") as file:
                json.dump(response.json(), file)
            with open(self.pathToProgress, "r") as file:
                    self.messages = json.load(file)
        else:
            print("Error:", response.status_code, response.text)
        print ("given instruct complete")

if __name__ == "__main__":
    Test().runningInput()
