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
import requests, json, time, openai, asyncio, os

class ChatGpt():
    def __init__(self, canAccessGpt = True, modelInfo = None, altUrl = None, testing = False):
        gptType = modelInfo if modelInfo is not None else "4"

        self.testing = testing

        self.specifyModel(gptType)
        
        self.gptAltAddress = (os.environ.get("ALT_GPT_URL", None) if altUrl is None
                        else altUrl)
        self.gptKey = os.environ.get("OPENAI_API_KEY", None)

        self.canAccessGpt = canAccessGpt
        
        self.timeLastCalled = 0
        self.scriptStartTime = time.time()

        self.testForGptFirewall()

    def testForGptFirewall(self):
        with open("platforms/GPT/testForFirewall.json", 'r') as f:
            data = json.load(f)

        temp = self.modelName

        self.specifyModel("3.5")

        if self.gptKey is None:
            if self.gptAltAddress is None:
                self.gptKey = input("Enter your OpenAI API Key or enter X if you do not wish to\n")
            else:
                # If we already have alt address and not gpt key, we assume to use alt address
                self.canAccessGpt = False

        if self.canAccessGpt:
            openai.api_key = self.gptKey

            response = self.getResponse(data) 

            if response == "ERROR":
                self.canAccessGpt = False
                print("Having problems using the python gpt api.\n" \
                    + "Swapping to alternative methods.")
                
                if self.gptAltAddress is None: 
                    self.gptAltAddress = input(
                        "Provide an address that can middleman " \
                        + "a connection to the gpt api.\n Generally this problem occurs" \
                            + "when there exists a firewall preventing access.\n" \
                            +"The CLEAR worker server can be webhosted and used to fix this.\n"
                        )

        self.specifyModel(temp)

    def specifyModel(self, message):
        if "3.5" in message :
            self.modelName = "gpt-3.5-turbo"
            self.waitingTime = 2

        elif "4" in message :
            self.modelName = "gpt-4"
            self.waitingTime = 5
        
        if self.testing:
            self.waitingTime = 15
        

    def getResponse(self, messages, timesTried = 0):
        async def _getResponse(messages = messages, timesTried = timesTried):
            if self.timeLastCalled + self.waitingTime > time.time() :
                await asyncio.sleep((self.timeLastCalled + self.waitingTime) - time.time())
                print("waiting ", self.waitingTime)
            
            self.timeLastCalled = time.time()

            if timesTried >= 3 : 
                print("bummers")
                return "ERROR"
            try :
                reply = (await self.queryGptApiDirect(messages) if self.canAccessGpt 
                            else self.queryGptIntermediate(messages))
                print (reply)
                return (reply if reply is not None
                            else await _getResponse(messages, 
                                timesTried=timesTried+1))
            except Exception as e :
                print(e)
                await asyncio.sleep(2)
                return await _getResponse(messages, timesTried=timesTried+1)
        return asyncio.run(_getResponse())
    
    # Handles the asynchronous GPT API calls and exceptions
    async def queryGptApiDirect(self, messages):
        try:
            response = await asyncio.wait_for(self.deliverQueryDirect(messages), 
                                              timeout=self.waitingTime * 2)
            return response["choices"][0]["message"]["content"]

        except asyncio.TimeoutError:
            print("The GPT API call has timed out.")
            return None

        except openai.error.InvalidRequestError as e:
            print("Exception with GPT: {}".format(str(e)))
            return None

        except openai.error.ServiceUnavailableError as e:
            print("Exception with GPT: {}".format(str(e)))
            return None

        except Exception as e:
            print("Exception with GPT: {}".format(str(e)))
            return None

    # Helper method to run the synchronous method queryGptDirect asynchronously
    async def deliverQueryDirect(self, messages):
        loop = asyncio.get_running_loop()

        def callingGpt(messages):
            return openai.ChatCompletion.create(
                model=self.modelName,
                messages=messages
            )
        
        return await loop.run_in_executor(None, callingGpt, messages)
        
    def queryGptIntermediate(self, messages):
        print(f"messages {messages}")

        url = f"{self.gptAltAddress}/chat"
        response = (requests.post(url,
         json={'string': messages, 'model' : self.modelName},
          timeout = self.waitingTime * 2))
        
        print (f"response is {response}")
        return (self.extract_message(response.content) 
          if response.status_code == 200 else None)

    def extract_message(self, response_content):
        # Parsing the response content as JSON
        decoded_content = response_content.decode('utf-8')
        content_json = json.loads(decoded_content)
        return content_json.get('message', '')