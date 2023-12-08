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

import socketio, time, requests
import threading, json, os
from datetime import datetime, timedelta
from platforms.GPT.ChatGpt import ChatGpt
from platforms.Llama2.Llama2 import Llama2

class Handler():
    def __init__(self, baseDir, url, model, gptAltUrl):
        self.sio = socketio.Client()
        self.URL = url        
        self.gptAltUrl = gptAltUrl
        serverThread = threading.Thread(target=self.startListen)
        self.chatReady = False
        self.givingInstruction = False
        self.baseDir = baseDir
        self.messages = []
        self.logPath = ""

        self.testMaxLedger = 13
        self.testHuman = True
        self.runningTests = True

        self.givePrompt = False
        self.conversationCount = 0
        self.NUM_LEDGERS_TILL_SWAP = 2

        self.setLLM(model)
        self.sio.on("instruction_updated")(self.givenInstruction)
        self.sio.on("instruction_requested")(self.instructionsRequested)
        self.sio.on("host_chat_updated")(self.chatInputted)
        self.sio.on("chat_reset_requested")(self.startNewConversation)
        self.sio.on("model_name_requested")(self.giveName)
        self.sio.on("readiness_requested")(self.giveReady)
        self.startTime = time.time()
        serverThread.start()

    def setLLM(self, key, addedInfo = None) :
        if hasattr(self, "lastKeyGiven") and \
            self.lastKeyGiven == key:
                self.languageModel.specifyModel(addedInfo)
                return

        self.lastKeyGiven = key
        LLM_MAP = {
            "LLaMA2": Llama2, 
            "ChatGpt": ChatGpt
            }

        # This occurs when app is run with arg for gpt alt url
        if key == "ChatGpt" and self.gptAltUrl is not None: 
            self.languageModel = LLM_MAP[key](altUrl=self.gptAltUrl,
                                               testing = self.runningTests)
        else:
            self.languageModel = LLM_MAP[key](testing = self.runningTests)
    
    def givenInstruction(self, message): 
        if self.givingInstruction: return 
        url = f'{self.URL}/instruction'
        print ("Instruction given to me!")

        response = requests.get(url)
        if response.status_code == 200:
            sharedJson = response.json()
            print(sharedJson)
            
            # If sending nothing
            if sharedJson is None:
                return

            self.droneType = sharedJson[0].pop("hardware", None)
            sharedJson = sharedJson[1:]

            # If provided LLM information in given instructions.
            # Currently, this functionality is only being used in testing
            llmInfoGiven = filterJson(sharedJson, "llmInfo")
            if llmInfoGiven is not None:
                self.processingLLMCommands(llmInfoGiven[0].get("content"))
                print("\nThe LLM info is \n",llmInfoGiven)
                sharedJson = sharedJson[1:]

            # If true, LLMs are allowed more inference time
            if self.droneType == "test":
                self.runningTests = True

            self.droneType += self.languageModel.modelName

            # sharedJson = sharedJson[1:]
            self.messages = sharedJson

            directory = os.path.join(self.baseDir, self.droneType)
            os.makedirs(directory, exist_ok=True)

            now = datetime.now()
            recent_dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and 
                           now - datetime.strptime(d, "%m-%d-%y_%H-%M") < timedelta(minutes=30)]

            if recent_dirs:
                chat_directory = os.path.join(directory, max(recent_dirs, key=lambda d: datetime.strptime(d, "%m-%d-%y_%H-%M")))
            else:
                timestamp = now.strftime("%m-%d-%y_%H-%M")
                chat_directory = os.path.join(directory, timestamp)
                os.makedirs(chat_directory, exist_ok=True)
        
            self.chat_directory = chat_directory
            self.logPath = self.generateChatFilePath()
            with open(self.logPath, "w") as file:
                    json.dump(self.messages, file)

            self.chatReady = True
        else:
            print("Error:", response.status_code, response.text)

    def generateChatFilePath(self, incrementHighest = 1):
        files = [f for f in os.listdir(self.chat_directory) if os.path.isfile(os.path.join(self.chat_directory, f)) and f.startswith("chat")]
        if not files:
            return os.path.join(self.chat_directory, "chat-0.json")
        
        print(files)
        
        max_index = max([int(f.split('-')[1].split('.')[0]) for f in files if '-' in f], default=0)

        print(f"The max index is {max_index}\n", f"chat-{max_index + incrementHighest}.json")
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
                self.logPath = self.generateChatFilePath()

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
            inputChat = response.json().get('prompt', None)
            fixedResponse = response.json().get('fixResponse', None)

            print("fixed response is: ", fixedResponse)
            
            # Fixing the previous ledger
            if fixedResponse is not None:
                # Cannot replace system definition
                if len(self.messages) > 1 :
                    print("old message\n", self.messages.pop())
                    self.messages.append({"role": "assistant", "content": fixedResponse})
                
                if self.runningTests:
                    if len(self.messages) > self.testMaxLedger:
                        self.startNewConversation()
                        return
                    
                    if self.givePrompt and len(self.messages) == 1:
                        inputChat += ("A human says, I want you to restart the simulation and" + 
                        "then message me hello, and then move to an object")

            if self.checkForCode(inputChat) :
                self.postChat(self.messages, code = inputChat)
                return

            self.messages.append({"role": "user", "content": inputChat}) 

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

        #Means something is broken
        if output == "ERROR" or resetConvo:
            print("generating new path")
            self.startNewConversation()
            output = 'conversationReset'

        timeInferring = (time.time() - init_time)
        print ("time to generate text : {}".format(timeInferring))

        url = '{}/clientChatInfo'.format(self.URL)
        response = requests.post(url, json={'response': output})
        print ("output is {}".format(output))
        print(response)
        return output

    def startNewConversation(self, message = None):
        
        if self.runningTests:
            self.conversationCount += 1
            if self.conversationCount > self.NUM_LEDGERS_TILL_SWAP:
                self.conversationCount = 0
                self.givePrompt = not self.givePrompt

        self.logPath = self.generateChatFilePath()

        #This allows the initial instruction to be preserved
        self.messages = [self.messages[0]]

        with open(self.logPath, "w") as file:
            json.dump(self.messages, file)
    
    def giveName(self, message=None) :
        print("my name is, ", self.languageModel.modelName)
        url = '{}/llmModel'.format(self.URL)
        response = requests.post(url, json={'model': self.languageModel.modelName})
        print("model name requested : ", response)

        #process input for codes or commands
    def givenInput(self, messages, code = None):
        if code is not None :
            self.processingLLMCommands(code)
            self.giveName()
            return "mess(command heard)"

        return self.languageModel.getResponse(messages)
    
    def processingLLMCommands(self, command):
        if "gpt" in command.lower():
                self.setLLM("ChatGpt", command.lower())

        elif "llama" in command.lower():
            self.setLLM("LLaMA2", command.lower())

def filterJson(arrDicts, value):
    arr = [d for d in arrDicts if d.get("role") == value]
    return arr if arr != [] else None