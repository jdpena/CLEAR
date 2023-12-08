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

from Handler import Handler
import argparse, os

parser = argparse.ArgumentParser()
defaultAddress = os.environ.get('WORKER_ADDRESS', "404")

parser.add_argument('--address', type=str, default=defaultAddress)
parser.add_argument('--altGptAddress', type=str, required=False)
parser.add_argument('--model', type=str, default="ChatGpt")

url = parser.parse_args().address

if url == "404":
    url = input("provide the address of the worker server")

model = parser.parse_args().model
altGptAddress = parser.parse_args().altGptAddress

PATH_TO_CHAT_HISTORY = "chatHistory"
platform = Handler(PATH_TO_CHAT_HISTORY, url, model, altGptAddress)

platform.disconnect()