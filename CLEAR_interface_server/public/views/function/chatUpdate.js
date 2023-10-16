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

// Select the chat input field and the chat submit button
let chatField = document.getElementById('chatInput');
let chatBox = document.getElementById('chat-content');
let mostRecentMessage;
let mostRecentUser;

// Add an event listener for 'Enter' key press in the chat input field
chatField.addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); // to prevent a newline from being entered in the chat box

    // Check if there's text to send
    if (this.value) {
      // Post the chat message
      addMessage('person', this.value);
      
      // sending it to llm
      postFeedback()

      // Clear the input field
      this.value = '';
    }
  }
});

let addMessage = (user, message) => {
  let newMessage = document.createElement('p');
  newMessage.innerHTML = `<strong>${user}:</strong> ${message}`;
  chatBox.appendChild(newMessage);
  chatBox.scrollTop = chatBox.scrollHeight; // To auto-scroll to the latest message

  // Store the message content as a string
  mostRecentUser = user
  mostRecentMessage = message;
};

// Function to append text to the latest message in the chatBox
let appendToLastMessage = (user, textToAppend) => {
  // Get the last message in the chat
  let lastMessageElement = chatBox.lastElementChild;

  // Check if there's at least one message in the chat
  if (lastMessageElement) {
    // Append the new text to the last message
    lastMessageElement.innerHTML += ` ${textToAppend}`;
  } else {
    // If there are no messages in the chat, add a new one
    let newMessageElement = document.createElement('p');
    newMessageElement.innerHTML = `<strong>${user}:</strong> ${textToAppend}`;
    chatBox.appendChild(newMessageElement);
  }

  // To auto-scroll to the latest message
  chatBox.scrollTop = chatBox.scrollHeight;
};



// Post feedback to the feedbackRoutes.js script
let postFeedback = () => {
  console.log(mostRecentMessage);
  let chat = {userChat: {user : mostRecentUser, message : mostRecentMessage}};

  fetch('/feedbackInfo', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ feedback: chat}),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Feedback posted:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
};

  // Listen for the 'chat_update' event
  socket.on('chat_update', (data) => {
    addMessage(data.user, data.message);
  });