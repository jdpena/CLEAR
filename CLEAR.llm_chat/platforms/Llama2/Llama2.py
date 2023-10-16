import requests, time, os
from platforms.Llama2.support import parseJson, reformat

class Llama2():
    def __init__(self):
        self.modelName = "LLaMA2"

        HUGGING_FACE_KEY = os.environ.get("HF_API_KEY", input("Enter your OpenAI API Key"))
        self.API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
        self.HEADERS = {
            "Authorization": f"Bearer {HUGGING_FACE_KEY}",
            "Content-Type": "application/json",
        }

        self.timeLastCalled = 0
        self.waitingTime = 3
    
    # This exists to uphold a standard between llm classes.
    def specifyModel(self, message):
        pass

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.HEADERS, json=payload)
        return parseJson(response.json())

    def getResponse(self, messages, code = None, timesTried = 0):
        if self.timeLastCalled + self.waitingTime > time.time() :
            time.sleep((self.timeLastCalled + self.waitingTime) - time.time())
            print("waiting ", self.waitingTime)

        if timesTried >= 3 : 
            print("bummers")
            return "ERROR"
        
        self.timeLastCalled = time.time()
        llmInput = reformat(messages)
        response = self.query(llmInput)

        if response == None:
            print("retrying")
            return self.getResponse(messages, timesTried = timesTried+1)
        
        print(response)
        return response