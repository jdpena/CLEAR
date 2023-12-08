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

const express = require('express');
const router = express.Router();
const bodyParser = require('body-parser');

module.exports = function (io) {
  let info = null;
  const jsonParser = bodyParser.json();
  const urlencodedParser = bodyParser.urlencoded({ extended: true });

  const processFeedback = (feedback, req, res) => {
    console.log("Feedback: ", feedback);
    info = feedback;
    io.emit('feedback_updated', 'New information has been uploaded.');
    res.status(200).json({ status: 'success', message: 'Information uploaded and saved to a variable.' });
  };

  router.post('/feedbackUnity', [jsonParser, urlencodedParser], (req, res) => {
    console.log("hello we are here")
    const feedback = req.body.feedback;
    processFeedback(feedback, req, res);
  });

  router.post('/feedbackInfo', jsonParser, (req, res) => {
    const feedback = req.body.feedback;
    processFeedback(feedback, req, res);
  });

  router.get('/feedbackInfo', (req, res) => {
    if (info) {
      res.json(info);
    } else {
      res.status(404).json({ status: 'error', message: 'No information found' });
    }
  });

  return router;
};
