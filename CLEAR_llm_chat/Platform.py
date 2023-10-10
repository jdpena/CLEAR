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

import socketio
import requests
import time
import threading
import json
import os
from datetime import datetime, timedelta

# from platforms.GPT.GPTOnlineOffNetwork import GPTOnlineOffNetwork
# from platforms.GPT.GPTOnline import GPTOnline
# from platforms.Llama2.Llama2 import Llama2

class ChatPlatform():
    def __init__(self, baseDir, url):
        self.sio = socketio.Client()
        self.URL = url        
        serverThread = threading.Thread(target=self.startListen)
        self.chatReady = False
        self.givingInstruction = False
        self.baseDir = baseDir
        self.messages = []
        self.logPath = ""
        self.testHuman = True
        self.sio.on("instruction_updated")(self.givenInstruction)
        self.sio.on("instruction_requested")(self.instructionsRequested)
        self.sio.on("host_chat_updated")(self.chatInputted)
        # self.sio.on("chat_reset_requested")(self.startNewConversation)
        self.sio.on("model_name_requested")(self.giveName)
        self.sio.on("readiness_requested")(self.giveReady)
        self.startTime = time.time()
        serverThread.start()

    def hourPassed(self):
        hourHasPassed = (time.time() - self.startTime) >= 3600
        if hourHasPassed:
            self.startTime = time.time()
        return hourHasPassed
    
    def givenInstruction(self, message): 
        if self.givingInstruction: return 
        url = f'{self.URL}/instruction'
        print ("Instruction given to me!")

        response = requests.get(url)
        if response.status_code == 200:
            sharedJson = response.json()
            print(sharedJson)
            self.droneType = sharedJson[0].pop("hardware", None)

            self.droneType += self.modelName

            sharedJson = sharedJson[1:]
            self.messages = sharedJson

            directory = os.path.join(self.baseDir, self.droneType)
            os.makedirs(directory, exist_ok=True)

            now = datetime.now()
            recent_dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and 
                           now - datetime.strptime(d, "%m-%d-%y_%H-%M") < timedelta(minutes=30)]

            if recent_dirs:  # if there's a directory that's less than 30 minutes old
                chat_directory = os.path.join(directory, max(recent_dirs, key=lambda d: datetime.strptime(d, "%m-%d-%y_%H-%M")))
            else:
                timestamp = now.strftime("%m-%d-%y_%H-%M")
                chat_directory = os.path.join(directory, timestamp)
                os.makedirs(chat_directory, exist_ok=True)
        
            self.chat_directory = chat_directory
            self.logPath = self.generateChatFilePath(incrementHighest=0)
            with open(self.logPath, "w") as file:
                    json.dump(self.messages, file)

            self.chatReady = True
        else:
            print("Error:", response.status_code, response.text)

    def generateChatFilePath(self, incrementHighest = 1):
        files = [f for f in os.listdir(self.chat_directory) if os.path.isfile(os.path.join(self.chat_directory, f)) and f.startswith("chat")]
        if not files:
            return os.path.join(self.chat_directory, "chat-0.json")
        
        max_index = max([int(f.split('-')[1].split('.')[0]) for f in files if '-' in f], default=0)
        return os.path.join(self.chat_directory, f"chat-{max_index + incrementHighest}.json")

    def instructionsRequested(self, message):
        print("Instructions Requested")
        if self.chatReady:
            try :
                self.givingInstruction = True
                # Update the chat directory name to the current time
                now = datetime.now()
                timestamp = now.strftime("%m-%d-%y_%H-%M")
                updated_chat_directory = (str(self.baseDir)
                                           + "/" + str(self.droneType)
                                             + "/" + str(timestamp))
                os.rename(self.chat_directory, updated_chat_directory)
                self.chat_directory = updated_chat_directory
                self.logPath = self.generateChatFilePath(incrementHighest=0)

                with open(self.logPath, 'r') as f:
                    data = json.load(f)

                url = '{}/instruction'.format(self.URL)
                response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
                print("sending instructions response is : {}".format(response))
                time.sleep(0.5)

            except Exception as e :
                print ("Instruction requests failed : {}".format(e))
            self.givingInstruction = False

            print("instructions sent")

    def startListen(self):
        print ("The URL being used : {}".format(self.URL))
        self.sio.connect(self.URL)
        print ("The URL used is : {}".format(self.URL))

    def disconnect(self):
        self.sio.disconnect()

    def giveReady(self, message) :
        url = '{}/readyInfo'.format(self.URL)
        requests.post(url,json={"llm_chat":"llm_chat"})

    def chatInputted(self, message):
        if not self.chatReady :
            return
        
        url = '{}/hostChatInfo'.format(self.URL)
        response = requests.get(url)
        print("chat inputted {}".format(response))

        if (response.status_code == 200) :
            inputChat = response.json()['string']

            if self.checkForCode(inputChat) :
                self.postChat(self.messages, code = inputChat)
                return

            # Testing human perception
            TESTING_HUMAN_RECEPTION = True
            STOP_EARLY = True
            
            # Will reset conversation after X responses
            # Helps make sure it does not take forever
            HOW_MANY_STEPS_ALLOWED_FOR_RUN = 16 

            HUMAN_MESSAGE = "I want you to restart the simulation and then message me hello, and then move to an object"

            MESSAGE_GIVEN = f". A human is telling you, {HUMAN_MESSAGE}"
            
            # if self.hourPassed(): self.testHuman = not self.testHuman
            
            if TESTING_HUMAN_RECEPTION and self.testHuman: 
                if len(self.messages) <= 2:
                    inputChat += MESSAGE_GIVEN
                    print("human is saying something")
                else :
                    print(f"There are {len(self.messages)} amount of messages")

            self.messages.append({"role": "user", "content": inputChat}) 

            if TESTING_HUMAN_RECEPTION \
                and len(self.messages) >= HOW_MANY_STEPS_ALLOWED_FOR_RUN :
                    outputChat = self.postChat(self.messages, resetConvo= True)
            else :
                outputChat = self.postChat(self.messages)

            if outputChat != "conversationReset":
                self.messages.append({"role": "assistant", "content": outputChat})

            with open(self.logPath, "w") as file:
                json.dump(self.messages, file)

        else:
            print("Error:", response.status_code, response.text)

    def checkForCode(self, message) :
        flag = "#code"

        if flag in message :
            return True
        
        return False

    def timeOut(self) :
        print("waiting to prevent gpt overload")
        time.sleep(self.timeWaitingAfterCall)
        
    def postChat(self, chat, code = None, resetConvo = False):
        init_time = time.time()
        output = self.givenInput(chat, code=code)

        #Means something has been broken
        if output == "Too many tokens" or resetConvo:
            print("generating new path")
            self.startNewConversation()
            output = 'conversationReset'

        timeInferring = (time.time() - init_time)
        print ("time to generate text : {}".format(timeInferring))

        url = '{}/clientChatInfo'.format(self.URL)
        response = requests.post(url, json={'string': output})
        print ("output is {}".format(output))
        print(response)
        return output

    def startNewConversation(self, message = None):
        self.logPath = self.generateChatFilePath()

        #This allows the initial instruction to be preserved
        self.messages = [self.messages[0]]

        with open(self.logPath, "w") as file:
            json.dump(self.messages, file)
