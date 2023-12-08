import requests, time, os, asyncio
from platforms.Llama2.support import parseJson, reformat

class Llama2():
    def __init__(self, testing = False):
        self.modelName = "LLaMA2"

        hfEnv = os.environ.get("HF_API_KEY")
        HUGGING_FACE_KEY = hfEnv if hfEnv is not None else input("enter your HuggingFace Token:\n")

        self.API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
        self.HEADERS = {
            "Authorization": f"Bearer {HUGGING_FACE_KEY}",
            "Content-Type": "application/json",
        }

        self.timeLastCalled = 0
        self.waitingTime = 3

        if testing: 
            self.waitingTime = 60

    
    # This exists to uphold a standard between llm classes.
    def specifyModel(self, message):
        pass

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.HEADERS, json=payload)
        return parseJson(response.json())

    def getResponse(self, messages, code = None, timesTried = 0):
        print("messages are \n", messages)
        async def _getResponse(messages = messages, timesTried = timesTried):
            if self.timeLastCalled + self.waitingTime > time.time() :
                await asyncio.sleep((self.timeLastCalled + self.waitingTime) - time.time())
                print("waiting ", self.waitingTime)

            if timesTried >= 3 : 
                print("bummers")
                return "ERROR"
            
            try:
                self.timeLastCalled = time.time()
                llmInput = reformat(messages)
                response = await self.queryApi(llmInput)

                if response is None:
                    return await _getResponse(messages, timesTried = timesTried+1)
                
                print(response)
                return response
        
            except Exception as e :
                print("Exception in getResponse ", e)
                await asyncio.sleep(2)
                return await _getResponse(messages, timesTried=timesTried+1)
            
        return asyncio.run(_getResponse())

    # Handles the asynchronous GPT API calls and exceptions
    async def queryApi(self, messages):
        try:
            response = await asyncio.wait_for(self.deliverQueryDirect(messages), 
                                              timeout=self.waitingTime * 2)
            return response

        except asyncio.TimeoutError:
            print("The API call has timed out.")
            return None

        except Exception as e:
            print("Exception with GPT: {}".format(str(e)))
            return None

    # Helper method to run the synchronous method queryGptDirect asynchronously
    async def deliverQueryDirect(self, messages):
        loop = asyncio.get_running_loop()

        def callingHuggingFace(messages):
            response = requests.post(self.API_URL, headers=self.HEADERS, json=messages)
            return parseJson(response.json())
        
        return await loop.run_in_executor(None, callingHuggingFace, messages)