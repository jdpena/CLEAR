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

from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers, torch, time

class Falcon7b() :
    def __init__(self) -> None:
        self.model = "tiiuae/falcon-7b"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto",
        )
    
    def givenInput(self, inputMessage) : 
        initTime = time.time()
        sequences = self.pipeline(
            str(inputMessage), 
            max_length=200,
            top_k=1,
            num_return_sequences=1,
            eos_token_id= self.tokenizer.eos_token_id,
        )
        print (time.time() - initTime)
        return sequences

if __name__ == "__main__" :
    falcon = Falcon7b()
    mesInput = ""
    while mesInput == " " :
        mesInput = input()
        falcon.generate(mesInput) 