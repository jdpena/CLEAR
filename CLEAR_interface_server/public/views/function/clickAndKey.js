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

const socket = io();
// Create a separate WebSocket connection to the audio server
const imageElement = document.getElementById('image');  // Get the image element
const statusElement = document.getElementById('status');  // Get the status div element
const dotElement = document.getElementById('dot');  // Get the dot element

let originalImageWidth, originalImageHeight;

// Key tracking objects
let currentKeys = {};
let previousKeys = {};


// Get the chat input field
const chatInput = document.getElementById('chatInput');

// Focus tracking variable
let isChatFocused = false;

// Listen for focus events on the chat input field
chatInput.addEventListener('focus', (e) => {
    isChatFocused = true;
});

// Listen for blur events on the chat input field
chatInput.addEventListener('blur', (e) => {
    isChatFocused = false;
});

// Helper function to POST keys to server
function postKeys() {
    fetch('/keys', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ keys: Object.keys(currentKeys) })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.log(error));
}

// Helper function to check if two objects are equal
function isEquivalent(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
}

// Only add the event listener after the window has loaded.
window.onload = () => {

    // Variables to store the original image dimensions
    imageElement.addEventListener('load', () => {
        const tempImage = new Image();  // Create a new Image object
        tempImage.onload = () => {  // Set the onload event handler
            originalImageWidth = tempImage.width;
            originalImageHeight = tempImage.height;
        };
        tempImage.src = imageElement.src;  // Set the source of the Image object
    });

    imageElement.addEventListener('click', (e) => {  
        const scaleX = originalImageWidth / imageElement.clientWidth;
        const scaleY = originalImageHeight / imageElement.clientHeight;
      
        const x = Math.round(e.offsetX * scaleX);
        const y = Math.round(e.offsetY * scaleY);
      
        console.log(`Clicked at (${x}, ${y})`);
    
        dotElement.style.display = 'block'; // Show the dot
    
        // Calculate relative position
        const rect = imageElement.getBoundingClientRect();
        const relativeX = e.clientX - rect.left;
        const relativeY = e.clientY - rect.top;

        console.log(`click screen at (${relativeX}, ${relativeY})`);

    
        dotElement.style.left = `${relativeX - 5}px`; // Position the dot
        dotElement.style.top = `${relativeY - 5}px`;
        

        // Emit the coordinates to your server
        setTimeout(() => {
            // User clicked the screen
            fetch('/considerClick', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ x, y })
            })
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.log(error));

            // requestAnimationFrame(() => {
            //     if (window.confirm('Are you sure you want to click here?')) {
            //         console.log(`Confirmed click at (${x}, ${y})`);
            //         dotElement.style.display = 'none';  // Hide the dot after confirmation
    
            //         fetch('/click', {
            //             method: 'POST',
            //             headers: {
            //                 'Content-Type': 'application/json'
            //             },
            //             body: JSON.stringify({ x, y })
            //         })
            //         .then(response => response.json())
            //         .then(data => console.log(data.message))
            //         .catch(error => console.log(error));
            //     } else {
            //         console.log('Click cancelled');
            //         dotElement.style.display = 'none';  // Hide the dot if the user cancels
            //     }
            // });
        }, 100);
    });

    // Listen for key down events
    window.addEventListener('keydown', (e) => {
        if(isChatFocused) {
            return;
        }    
        
        // Record the key press
        currentKeys[e.key.toLowerCase()] = true;

        // Log the keys that are currently pressed
        console.log(`Keys pressed: ${Object.keys(currentKeys).join(', ')}`);

        // If keys state has changed, Post the keys to the server
        if (!isEquivalent(currentKeys, previousKeys)) {
            postKeys();
            previousKeys = {...currentKeys};
        }
    });

    // Listen for key up events
    window.addEventListener('keyup', (e) => {
        if(isChatFocused) {
            return;
        }
    
        // Remove the key release
        delete currentKeys[e.key.toLowerCase()];

        // Log the keys that are currently pressed
        console.log(`Keys pressed: ${Object.keys(currentKeys).join(', ')}`);

        // If keys state has changed, Post the keys to the server
        if (!isEquivalent(currentKeys, previousKeys)) {
            postKeys();
            previousKeys = {...currentKeys};
        }
    });

    socket.on('roboClick_received', (coordinates) => {
        console.log(`RoboClick received at (${coordinates.x}, ${coordinates.y})`);
    
        dotElement.style.display = 'block'; // Show the dot
    
        // Calculate the position on the scaled image
    
        const scaleX =  originalImageWidth / imageElement.clientWidth;
        const scaleY = originalImageHeight / imageElement.clientHeight;
    
        console.log(`RoboClick scale at (${scaleX}, ${scaleY})`);
    
     // Calculate the position on the screen
     const screenX = Math.round(coordinates.x / scaleX);
     const screenY = Math.round(coordinates.y / scaleY);
 
     console.log(`RoboClick screen at (${screenX}, ${screenY})`);
 
     // Position the dot considering the image's offset
     dotElement.style.left = `${screenX}px`;
     dotElement.style.top = `${screenY}px`;

    //  dotElement.style.left = `${20}px`;
    //  dotElement.style.top = `${20}px`;
    
        // Confirm the click
        setTimeout(() => {
            requestAnimationFrame(() => {
                if (window.confirm('Are you sure you want to click here?')) {
                    console.log(`Confirmed RoboClick at (${coordinates.x}, ${coordinates.y})`);
                    dotElement.style.display = 'none';  // Hide the dot after confirmation
    
                    // In your scenario, you might not need to send a click back to the server
                    // as the server already knows about the RoboClick. But if needed, here is how you would do it:
                    fetch('/click', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(coordinates)
                    })
                    .then(response => response.json())
                    .then(data => console.log(data.message))
                    .catch(error => console.log(error));
                } else {
                    console.log('RoboClick cancelled');
                    dotElement.style.display = 'none';  // Hide the dot if the user cancels
    
                    // Notify the server of the cancelled click
                    fetch('/cancelRoboClick', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(coordinates)
                    })
                    .then(response => response.json())
                    .then(data => console.log(data.message))
                    .catch(error => console.log(error));
                }
            });
        }, 500);
    });    
}

socket.on('image_updated', (msg) => {
    // Make a GET request to /image route
    fetch('/webImage')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            imageElement.src = `data:image/webp;base64,${data.image}`;  // update the image source
        } else {
            console.log(data.message);
        }
    })
    .catch(error => console.log(error));
});




