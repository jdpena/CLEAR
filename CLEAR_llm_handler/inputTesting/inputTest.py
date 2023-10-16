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

import socketio, requests, base64, threading, json, os

class Test:
    def __init__(self):
        self.sio = socketio.Client()

        self.URL = os.environ.get('WORKER_ADDRESS', input("provide an address"))

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
        # Perform GET request to XXXRL
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
