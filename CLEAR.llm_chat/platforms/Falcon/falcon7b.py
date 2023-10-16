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