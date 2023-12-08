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

// Keys are related to movement
const MOVEMENT_KEYS = ['w','a','s','d','q','e',' ','.','0','x']

function isMovementKey(key) {
    return MOVEMENT_KEYS.includes(key);
}

module.exports = function (io) {
    let keysPressed = [];
    let userClick = null;
    let consideredClick = null;

    router.post('/userMessage', (req, res) => {
        const USER = req.body.user;
        let messageSent = req.body.message;

        const FROM_HUMAN = req.body.fromHuman;

        const FROM_AUDIO = req.body.createdFromAudio;

        // Check if message exists and is not empty
        if (messageSent && messageSent.trim()) {
            // Emit a socket.io event to all connected clients
            // will be caught by front end
            if (FROM_AUDIO)
                io.emit('chat_update', { user: USER, message: messageSent, fromAudio: "true"});
            else
                io.emit('chat_update', { user: USER, message: messageSent });
            
            // To be caught by coordinator
            if (FROM_HUMAN) 
                io.emit('user_chat_update', { user: USER, message: messageSent });
            

            res.status(200).json({ status: 'success', message: 'Message received and sent to chat.' });
        } else {
            res.status(400).json({ status: 'error', message: 'No message found in request.' });
        }
    });
    
    // proposed click from user
    router.post('/considerClick', (req, res) => {  
        const coordinates = req.body; 
        consideredClick = coordinates;
        io.emit('consideringClick', consideredClick);
        res.status(200).json({ status: 'success', message: 'consideringClick' });
    });

    router.get('/considerClick', (req, res) => {
        if (consideredClick) {
            res.json({ click: consideredClick });
        } else {
            res.status(404).json({ status: 'error', message: 'No consideredClick' });
        }
    });

    router.post('/roboClick', (req, res) => {  
        const coordinates = req.body;  // Get the coordinates from the request body
        console.log(coordinates);
    
        // Save the coordinates to 'userClick' just like in the '/click' route
        userClick = coordinates;
    
        // Emit an event that the frontend will listen to
        io.emit('roboClick_received', coordinates);
    
        res.status(200).json({ status: 'success', message: 'RoboClick coordinates received and saved.' });
    });
    
    router.post('/cancelRoboClick', (req, res) => {  
        io.emit('roboClick_cancelled', 'big fun');
        res.status(200).json({ status: 'success', message: 'RoboClick cancelled' });
    });

    router.post('/click', (req, res) => {  // Create a new route to receive click coordinates
        userClick = req.body;  // Save the click coordinates
        console.log(userClick);
        consideredClick = null;
        io.emit('click_updated', 'coordinate uploaded.');
        res.status(200).json({ status: 'success', message: 'Click coordinates received and saved.' });
    });

    router.get('/click', (req, res) => {
        if (userClick) {
            res.json({ click: userClick });
        } else {
            res.status(404).json({ status: 'error', message: 'No user click' });
        }
    });

    router.post('/keys', (req, res) => {
        const keys = req.body.keys;
        if (keys) {
            keysPressed = keys.filter(isMovementKey);  // Replace the existing keys with the new keys
            console.log(keysPressed)
            io.emit('keys_updated', 'key uploaded.');
            res.json({ message: 'Keys updated.' });
        } else {
            res.status(404).json({ status: 'error', message: 'No keys' });
        }
    });

    router.get('/keys', (req, res) => {
        res.json({ keys: keysPressed });
    });

    router.post('/describeCommand', (req, res) => {
        const commandDescription = req.body.command;
        io.emit('chat_update', { user: 'robot', message: commandDescription});
        console.log("command_sent: ", commandDescription);
        res.status(200).json({ status: 'success', message: 'Command description uploaded'});
    });

  return router;
};