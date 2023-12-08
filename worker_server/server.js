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
const http = require('http');
const cors = require('cors');
const { Server } = require('socket.io');
const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",  // Allows all origins
    methods: ["GET", "POST", "PUT", "DELETE"],  // Allows all HTTP methods
    allowedHeaders: "*",  // Allows all headers
    credentials: true
  }
});

app.use(cors());
app.disable('x-powered-by');
app.use((req, res, next) => {
  res.removeHeader("X-Frame-Options"); // Disable X-Frame-Options
  next();
});

const imageRoutes = require('./routes/imageRoutes');
const depthRoutes = require('./routes/depthRoutes');
const contextRoutes = require('./routes/contextRoutes');
const hostChatRoutes = require('./routes/hostChatRoutes');
const clientChatRoutes = require('./routes/clientChatRoutes');
const instructionRoutes = require('./routes/instructionRoutes');
// const gptRoutes = require('./routes/gptRoutes');
const downloadRoutes = require('./routes/downloadRoutes');
const readyRoutes = require('./routes/readyRoutes');

app.use(express.json({ limit: '1000mb' }));
app.use(express.static('public'));
app.use(imageRoutes(io));
app.use(depthRoutes(io));
app.use(contextRoutes(io));
app.use(hostChatRoutes(io));
app.use(clientChatRoutes(io));
app.use(instructionRoutes(io));
// app.use(gptRoutes(io));
app.use(downloadRoutes(io));
app.use(readyRoutes(io));

io.on('connection', (socket) => {
  console.log('A user connected');
  io.emit('connection', 'A user connected');

  socket.on('disconnect', () => {
    console.log('A user disconnected');
    io.emit('disconnection', 'A user disconnected');
  });
});

const port = process.env.PORT || 9999;
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});