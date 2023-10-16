import cv2
import numpy as np
import requests
import socketio
import threading
import time
import random

class ServerHandler():
    def __init__(self) -> None:
        self.sio = socketio.Client()
        self.URL = 'http://localhost:7070'
        self.sio.on("image_updated")(self.imageUpdated)
        self.sio.on("feedback_updated")(self.feedbackUpdated)
        self.GOOD_CODE = 200
        self.image = None
        self.context = None

        # For having a persistent connection
        self.session = requests.Session()
        serverThread = threading.Thread(target= self.startListen, daemon=True)
        serverThread.start()
        
        self.sendInstructions()

    def startListen(self):
        # Event listeners
        self.sio.connect(self.URL)
    
    def disconnect(self):
        self.sio.disconnect()

    def imageUpdated(self, message):
        url = "{}/image".format(self.URL)
        response = self.session.get(url, stream=True)
        if not response.status_code == self.GOOD_CODE:
            print("Failed to get image: status code", response.status_code)
            return

        # Convert binary data to numpy array
        nparr = np.frombuffer(response.content, np.uint8)

        # Decode numpy array to image
        self.image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def getImage(self) :
        while type(self.image) == type(None) : 
            time.sleep(0.1)
        return self.image
    
    def makeArray(self) :
        arr =[0,0,0,0] 

        for i in range(len(arr)) :
            sign = 1 if random.random() > 0.5 else -1
            arr[i] = random.random() *5 * sign 
        
        return {"velocities" : arr}
    
    def askRotation(self) :
        return {"Command": "clientRotation"}


    def feedbackUpdated(self, message) :
        url = '{}/feedbackInfo'.format(self.URL)
        response = self.session.get(url)

        if response.status_code == 200:
            info = response.json()['clientRotation']
            if info != None :
                print (info)
        else:
            print("Error:", response.status_code, response.text)
        
        
    def sendInstructions(self):
        url = '{}/instructionInfo'.format(self.URL)
        data = {}
        data.update(self.makeArray())
        data.update(self.askRotation())
        response = self.session.post(url, json=data)

test = ServerHandler()
while True: 
    if test.image is not None:
        test.sendInstructions()
        cv2.imshow("img", test.image)
        cv2.waitKey(1)
    time.sleep(0.1)