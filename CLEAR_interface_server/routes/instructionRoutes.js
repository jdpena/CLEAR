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

module.exports = function (io) {
  let velocity = null;
  let command = null

  router.post('/instructionInfo', (req, res) => {
    const inputVelocities = req.body.velocities;
    const inputCommand = req.body.Command;

    velocity = inputVelocities;
    command = inputCommand;

    io.emit('instruction_updated', 'New velocities have been uploaded.');
    res.status(200).json({ status: 'success', message: 'Velocities uploaded and saved to a variable.' });
  });

  router.get('/instructionInfo', (req, res) => {
    let shouldSend = false;
    let data = {}

    if (velocity) {
      data = { ...data, velocities: velocity };
      velocity = null;
      shouldSend = true;
    } 

    if (command) {
      data = { ...data, Command: command }; 
      command = null;
      shouldSend = true;
    } 

    if (shouldSend) {
      res.json(data);
    } else {
      res.status(404).json({ status: 'error', message: 'No velocities found' });
    }
  });

  return router;
};