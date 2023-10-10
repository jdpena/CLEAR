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

import openai, os

class GPTOnline():
    def __init__(self):
        openai.api_key = os.environ("gptAI")
        openai.api_key = "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"

    def givenInput(self, messages):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            reply = response["choices"][0]["message"]["content"]

            return reply

        except openai.error.InvalidRequestError as e:
            print("Exception with GPT: {}".format(str(e)))
            return "Too many tokens"

        except openai.error.ServiceUnavailableError as e:
            print("Exception with GPT: {}".format(str(e)))
            return "no"
