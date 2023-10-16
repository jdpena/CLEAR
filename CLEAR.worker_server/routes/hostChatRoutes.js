const express = require('express');
const router = express.Router();

module.exports = function (io) {
  let hostChatInfo = null;

  router.post('/hostChatInfo', (req, res) => {
      const inputString = req.body.string;
      hostChatInfo = inputString;
      // console.log('POST /hostChatInfo, hostChatInfo is now:', hostChatInfo);
      io.emit('host_chat_updated', 'A new string has been uploaded.');
      res.status(200).json({ status: 'success', message: 'String uploaded and saved to a variable.' });
  });

  router.get('/hostChatInfo', (req, res) => {
    // console.log('GET /hostChatInfo, hostChatInfo is:', hostChatInfo);
    if (hostChatInfo) {
      res.json({ string: hostChatInfo });
      hostChatInfo = null;
    } else {
      res.status(404).json({ status: 'error', message: 'No string found' });
    }
  });

  return router;
};

