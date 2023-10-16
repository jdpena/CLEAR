//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;                      //stream from getUserMedia()
var rec;                            //Recorder.js object
var input;                          //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record

let shoudAppend = false;

var toggleButton = document.getElementById("toggleMic");
var isRecording = false; // A flag variable to track the recording status

// Add an event to the button
toggleButton.addEventListener("click", function() {
    if(!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
    isRecording = !isRecording; // Toggle the recording status
});

// Interval variable to send audio data every 3 seconds
var sendAudioDataInterval;

function createRecorder(stream) {
    /* use the stream */
    input = audioContext.createMediaStreamSource(stream);

    /* 
        Create the Recorder object and configure to record mono sound (1 channel)
        Recording 2 channels  will double the file size
    */
    rec = new Recorder(input,{numChannels:1});

    //start the recording process
    rec.record();
}

function startRecording() {
    toggleButton.src = "./resources/microphoneRed.png"; 

    console.log("recordButton clicked");

    toggleButton.textContent = "Stop Recording";

    var constraints = { audio: true, video:false }

    toggleButton.disabled = false;

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        audioContext = new AudioContext();

        gumStream = stream;

        // create the recorder
        createRecorder(stream);

        console.log("Recording started");

        // Start sending audio data every 2 seconds
        sendAudioDataInterval = setInterval(function(){
            // create the wav blob and send to server
            rec.exportWAV(sendDataToFlaskServer);

            // stop the recording
            rec.stop();

            // create a new recorder
            createRecorder(gumStream);
        }, 5000);

    }).catch(function(err) {
        toggleButton.disabled = false;
    });
}

function stopRecording() {
    toggleButton.src = "./resources/microphone.png"; 

    console.log("stopButton clicked");

    toggleButton.textContent = "Start Recording";

    toggleButton.disabled = false;

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    // Stop sending audio data
    clearInterval(sendAudioDataInterval);

    //create the wav blob and send it to server one last time
    rec.exportWAV(sendDataToFlaskServer);

    shoudAppend = false;
}



function sendDataToFlaskServer(blob) {
    let data = new FormData();
    data.append('file', blob, 'record.wav');

    fetch(url, {
        method: 'POST',
        body: data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }) 
    .then(response => {
        console.log('Successfully sent the file to the server!', response);
        // Assuming the response contains a 'user' and 'message' field
        if(response.user && response.message){
            if (shoudAppend) {
                appendToLastMessage(response.user, response.message);
            } else {
                shoudAppend = true;
                addMessage(response.user, response.message);
            }
        } else {
            if (shoudAppend) {
                // Post feedback posts last message in chat
                postFeedback();
                shoudAppend = false;
            }
        }
    })
    .catch(e => {
        console.error('An error occurred while sending the file to the server:', e);
    });
}