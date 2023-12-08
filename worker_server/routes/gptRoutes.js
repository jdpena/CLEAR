// XXX A. XXX. Distribution is unlimited.

// XXX supported XXXnder XXX of XXX for 
// XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
// findings, XXX 
// of the author(s) XXX the XXX 
// XXX of XXX for XXX and XXX.

// © 2023 XXX.

// XXX.XXX-11 Patent Rights - XXX (May 2014)

// The software/XXX-Is basis

// XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
// XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
// U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
// XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
// XXX XXX.S. XXX may violate any copyrights that exist in this work.

const { Configuration, OpenAIApi } = require("openai");
const express = require('express');
const router = express.Router();

module.exports = function (io) {
  
  const configuration = new Configuration({
    // Going to have to manually enter this if launch on web
    organization: "YOUR ORGANIZATION Key",
    apiKey: "YOUR GPT API KEY",
  });
  const openai = new OpenAIApi(configuration);
  let gptOutput = null;
  
  router.post('/chat', async (req, res) => {
    const chatinput = req.body.string;
    const model = req.body.model;

    let generatedChat = null;

    // set a timeout of 10 seconds
    const timeout = new Promise((_, reject) => {
      const id = setTimeout(() => {
        clearTimeout(id);
        reject('Server timed out after 10s');
      }, 10000);
    });

    try {
      generatedChat = await Promise.race([
        openai.createChatCompletion({
          "model": model,
          "messages": chatinput,
          "max_tokens": 48
        }),
        timeout
      ]);

      if (generatedChat.data && generatedChat.data.choices && generatedChat.data.choices.length > 0) {
        gptOutput = generatedChat.data.choices[0].message.content;
        io.emit('chat_updated', 'Client is requesting instructions.');
        res.status(200).json({ status: 'success', message: gptOutput});
      } 
      else {
        res.status(500).json({ status: 'error', message: 'Failed to generate chat'});
      }
    } 
    catch (err) {
      console.error(err);
      if(err.toString().includes('Server timed out after 10s')){
        res.status(500).json({ status: 'error', message: 'Server timed out after 10s'});
      } else {
        res.status(500).json({ status: 'error', message: 'Failed to generate chat'});
      }
    }
  });
  
  return router;
};