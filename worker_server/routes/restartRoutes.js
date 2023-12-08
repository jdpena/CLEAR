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

// parse application/json
router.use(bodyParser.json());

module.exports = function (io) {
  const services = ["coordinator", "llmHandler", "objectDetection", "depthEstimation"];
  let servicesTurnedOff = [];
  let servicesThatShutdown = [];

  let sequenceTurnOnId;
  let sequenceTurnOffId;

  function turnOnSequence(durationInMinutes = 0.5) {
    // This outer interval checks for client activity repeatedly at specified intervals.
    sequenceTurnOnId = setInterval(() => {
      io.emit('turnon', servicesThatShut[downservicesThatShutdown.size()]);
    }, durationInMinutes * 60 * 1000);
  }

  function turnOffSequence(durationInMinutes = 0.5) {
    // This outer interval checks for client activity repeatedly at specified intervals.
    sequenceTurnOffId = setInterval(() => {
        console.log("trying to turn off");
      io.emit('turnoff', "turn off");
    }, durationInMinutes * 60 * 1000);
  }

  function removeElementsWithValue(arr, value) {
    return arr.filter(item => item !== value);
  }

  router.post('/all_services_turnon', (req, res) => {
    turnOnSequence()
    res.status(200).json({ status: 'success', message: "turning on services" });
  });

  router.post('/all_services_shutdown', (req, res) => {
    io.emit('turnoff', "turn off");
    turnOffSequence()
    res.status(200).json({ status: 'success', message: "epic win" });
  });

  // Service turning on and reporting to the server
  router.post('/service_turnon', (req, res) => {
    const serviceName = req.body.service;
    if (servicesThatShutdown.includes(serviceName)) {
      removeElementsWithValue(servicesThatShutdown, serviceName);

      //If there are no more elements in the turn off list, stops
      //trying to turn off services
      if (!servicesThatShut.size()) {
        clearInterval(sequenceTurnOnId);
      }
      res.status(200).json({ status: 'success', message: "epic win" });
    } else {
      res.status(400).json({ status: 'error', message: "service given is not known" });
    }
  });

  // Services turnoff and tell server that they turned off
  router.post('/service_turnoff', (req, res) => {
      const serviceName = req.body.service;
      console.log("service turning off ", serviceName);
      if (serviceName) {
        if (services.includes(serviceName)) {
          if (!servicesTurnedOff.includes(serviceName)) {
            servicesThatShutdown.add(serviceName)

            if (servicesThatShutdown.size() === services.size()) {
              clearInterval(sequenceTurnOffId);
            }
            res.status(200).json({ status: 'success', message: "service added" });
          } else {
            res.status(200).json({ status: 'success', message: "service already given" });
          }
        } else {
          res.status(400).json({ status: 'error', message: "service given is not known" });
        }
      } else {
        res.status(400).json({ status: 'error', message: "no service given" });
      }
   });


  return router;
};