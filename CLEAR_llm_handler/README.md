# CLEAR_llm_chat

CLEAR llm chat is responsible for handling a given large language model (LLM) tasked with the decision-making processes of the CLEAR project. This service connects to the worker server to receive prompts. These prompts will then be appended to a conversation ledger, which is given to the LLM. The LLM’s response will then be relayed to the worker server and appended to the conversation ledger. Additionally, it preserves and catalogs the conversations.
 
Run CLEAR_llm_chat on a Windows or Unix system in a Python 3.8 interpreter accompanied by the packages expressed in setup/requirements.txt. To run the service, use
 
``python main.py --address <address> --platform <offNetwork||onNetwork>``

-----

XXX A. XXX. Distribution is unlimited.
 
XXX supported XXXnder XXX of XXX for XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions, findings, conclusions or recommendations XXX(s) XXX the XXX XXX of XXX for XXX and XXX.

© 2023 XXX.

XXX.XXX-11 Patent Rights - XXX (May 2014)

The software/XXX-Is basis

SPDX-License-Identifier: XXX
