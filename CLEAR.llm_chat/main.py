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