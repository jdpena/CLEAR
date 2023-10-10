import json
import requests
headers = {"Authorization": f"Bearer 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"}
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query(
    {
        "inputs": {
            "question": "What's my name?",
            "context": "My name is Clara and I live in Berkeley.",
        }
    }
)
print(data)