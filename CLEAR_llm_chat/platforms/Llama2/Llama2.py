import requests, time, json
from platforms.Llama2.support import formatEntries, separateEntries, parseJson, reformat
from Platform import ChatPlatform

class Llama2(ChatPlatform):
    def __init__(self, baseDir = None, url = None):
        super().__init__(baseDir, url)
        self.modelName = "llama2"

        self.API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
        self.HEADERS = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
        }

        self.timeLastCalled = 0
        self.waitingTime = 3

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.HEADERS, json=payload)
        return parseJson(response.json())

    def givenInput(self, messages, code = None, timesTried = 0):
        if self.timeLastCalled + self.waitingTime > time.time() :
            time.sleep((self.timeLastCalled + self.waitingTime) - time.time())
            print("waiting ", self.waitingTime)

        if timesTried >= 3 : 
            print("bummers")
            return "Too many tokens"
        
        self.timeLastCalled = time.time()
        llmInput = reformat(messages)
        response = self.query(llmInput)

        if response == None:
            print("retrying")
            return self.givenInput(messages, timesTried = timesTried+1)
        
        print(response)
        return response
    
    def giveName(self, message=None) :
        url = '{}/llmModel'.format(self.URL)
        response = requests.post(url, json={'model': self.modelName})
        print("model name requested : ", response)

####################################
if __name__ == "__main__":
    llama = Llama2()
    # Open the file for reading
    with open('chat-0.json', 'r') as file:
        data = json.load(file)

    system_entries, other_entries = separateEntries(data)

    information = formatEntries(system_entries, other_entries) + "[/INST]"

    # Construct the prompt
    prompt = {
        "inputs": information,
        "parameters": {
            "max_length": 16384,
            "temperature": 1,
            "top_k": 2000
        },
        "options": {
            "use_cache": False,
            "wait_for_model": True
        }
    }

    print(prompt)
    print("\n\n\n\n")

    # Send the prompt and get the output
    output = llama.givenInput(prompt)
    print(output)

    # Open the file for appending
    with open('chat-0.json', 'a') as file:
        new_entry = {"role": "assistant", "content": output}
        json.dump(new_entry, file)

