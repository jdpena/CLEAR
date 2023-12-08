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

const socket = io();

const userConnections = document.getElementById('user-connections');
const requestLog = document.getElementById('request-log');
const connectedUsersElement = document.getElementById('connectedUsers');

let connectedUsers = parseInt(localStorage.getItem('connectedUsers')) || 0;

connectedUsersElement.textContent = `Connected Users: ${connectedUsers}`;

socket.on('connection', (msg) => {
    userConnections.textContent = msg;
    connectedUsers += 1;
    localStorage.setItem('connectedUsers', connectedUsers);
    connectedUsersElement.textContent = `Connected Users: ${connectedUsers}`;
});

socket.on('disconnection', (msg) => {
    userConnections.textContent = msg;
    connectedUsers += 1;
});

socket.on('image_updated', (msg) => {
    const li = document.createElement('li');
    li.textContent = msg;
    requestLog.appendChild(li);
});

socket.on('depth_updated', (msg) => {
    const li = document.createElement('li');
    li.textContent = msg;
    requestLog.appendChild(li);
});

socket.on('context_updated', (msg) => {
    const li = document.createElement('li');
    li.textContent = msg;
    requestLog.appendChild(li);
});

socket.on('host_chat_updated', (msg) => {
    const li = document.createElement('li');
    li.textContent = msg;
    requestLog.appendChild(li);
});

socket.on('client_chat_updated', (msg) => {
    const li = document.createElement('li');
    li.textContent = msg;
    requestLog.appendChild(li);
});

socket.on('instruction_updated', (msg) => {
    const li = document.createElement('li');
    li.textContent = msg;
    requestLog.appendChild(li);
});
