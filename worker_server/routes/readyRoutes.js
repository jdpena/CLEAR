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
const bodyParser = require('body-parser');
const router = express.Router();

// parse application/x-www-form-urlencoded
router.use(bodyParser.urlencoded({ extended: true }));


//this script is for use by the setup application
// parse application/json
router.use(bodyParser.json());

module.exports = function (io) {
  let objectDetection = null;
  let depthPerception = null;
  let llmWorker = null;

  router.post('/readyInfo', (req, res) => {
      const ObjectDetection = req.body.object_detection;
      const DepthPerception = req.body.depth_perception;
      const LLM = req.body.llm_chat;

      if (ObjectDetection) {
        objectDetection = ObjectDetection;
      }

      if (DepthPerception) {
        depthPerception = DepthPerception;
      }

      if (LLM) {
        llmWorker = LLM;
      }

      if (objectDetection && depthPerception 
        && llmWorker) {
          io.emit('System_Ready', 'READY!');
      }

      res.status(200).json({ status: 'success', 
      message: 'readiness made known' });
  });

  router.post('/readyrequest', (req, res) => {
      io.emit('readiness_requested', 'uReady?');
      res.status(200).json({ status: 'success', message: "epic win" });
  });

  router.post('/readyreset', (req, res) => {
        objectDetection = false;
        depthPerception = false;
        llmWorker = false;
        res.status(200).json({ status: 'success', message: "epic win" });
  });

  router.get('/readyInfo', (req, res) => {
      let output = "";
      let ready = true;
      const projectName = "CLEAR"

      if (objectDetection) {
          output += projectName+"_object_detection is READY ";
      } else {
          output += projectName+"_object_detection is NOT ready ";
          ready = false;
      }

      if (depthPerception) {
          output += projectName+"_depth_perception is READY ";
      } else {
          output += projectName+"_depth_perception is NOT ready ";
          ready = false;
      }

      if (llmWorker) {
          output += projectName+"_llm_chat is READY ";
      } else {
          output += projectName+"_llm_chat is NOT ready ";
          ready = false;
      }

      if (ready) {
              res.status(200).json({ status: 'success', message: output });
      } else {
          res.status(400).json({ status: 'error', message: output });
      }
  });
  

  return router;
};