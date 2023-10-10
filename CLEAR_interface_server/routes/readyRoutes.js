// DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

// This material is based upon work supported by the Under Secretary of Defense for 
// Research and Engineering under Air Force Contract No. FA8702-15-D-0001. Any opinions,
// findings, conclusions or recommendations expressed in this material are those 
// of the author(s) and do not necessarily reflect the views of the Under 
// Secretary of Defense for Research and Engineering.

// © 2023 Massachusetts Institute of Technology.

// Subject to FAR52.227-11 Patent Rights - Ownership by the contractor (May 2014)

// The software/firmware is provided to you on an As-Is basis

// Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 
// 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, 
// U.S. Government rights in this work are defined by DFARS 252.227-7013 or 
// DFARS 252.227-7014 as detailed above. Use of this work other than as specifically
// authorized by the U.S. Government may violate any copyrights that exist in this work.

const express = require('express');
const bodyParser = require('body-parser');
const router = express.Router();

// parse application/x-www-form-urlencoded
router.use(bodyParser.urlencoded({ extended: true }));

// parse application/json
router.use(bodyParser.json());

module.exports = function (io) {
  let coordinatorReady = null;
  let droneReady = null;
  let successfulApps = new Set();

  router.post('/readyInfo', (req, res) => {
      const coordinator = req.body.coordinator;
      const drone = req.body.drone;

      if (drone) {
          droneReady = drone;
      }

      if (coordinator) {
        coordinatorReady = coordinator;
      }

      if (droneReady && coordinatorReady) {
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
      coordinatorReady = false;
      droneReady = false;
      successfulApps.clear();
      res.status(200).json({ status: 'success', message: "epic win" });
  });

  router.get('/readyInfo', (req, res) => {
      let output = "";
      let ready = true;
      const projectName = "CLEAR";

      if (droneReady) {
          output += projectName+"_robot is READY ";
      } else {
          output += projectName+"_robot is NOT ready ";
          ready = false;
      }

      if (coordinatorReady) {
          output += projectName+"_coordinator is READY ";
      } else {
          output += projectName+"_coordinator is NOT ready ";
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