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
const https = require('https');  
const fs = require('fs');  
const cors = require('cors');
const { Server } = require('socket.io');
const app = express();

// Read the key and certificate
const privateKey = fs.readFileSync('security/key.pem', 'utf8');
const certificate = fs.readFileSync('security/cert.pem', 'utf8');

const credentials = { 
  key: privateKey, 
  cert: certificate,
  passphrase: 'spot'
};
const server = https.createServer(credentials, app); 

const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: "*",
    credentials: true
  }
});

app.use(cors());
app.disable('x-powered-by');
app.use((req, res, next) => {
  res.removeHeader("X-Frame-Options"); 
  next();
});

const imageRoutes = require('./routes/imageRoutes');
const feedbackRoutes = require('./routes/feedbackRoutes');
const instructionRoutes = require('./routes/instructionRoutes');
const readyRoutes = require('./routes/readyRoutes');
const controllerRoutes = require('./routes/controllerRoutes');

app.use(express.json({ limit: '10000mb' }));
app.use(express.static('public'));
app.use(imageRoutes(io));
app.use(feedbackRoutes(io));
app.use(instructionRoutes(io));
app.use(readyRoutes(io));
app.use(controllerRoutes(io));

io.on('connection', (socket) => {
  console.log('A user connected');
  io.emit('connection', 'A user connected');

  socket.on('stream', (buffer) => {
    // broadcast the audio data to all clients
    socket.emit('stream', buffer);
  });

  socket.on('disconnect', () => {
    console.log('A user disconnected');
    io.emit('disconnection', 'A user disconnected');
  });
});

const port = process.env.PORT || 7070;
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

