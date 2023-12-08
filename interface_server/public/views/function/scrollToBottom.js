// This file is to make sure the chat scrolls to the bottom when new chat is added 

const chat = document.querySelector("#chat-content");
const anchor = document.querySelector("#anchor");
const config = { childList: true };

const callback = function (mutationsList, observer) {
  for (let mutation of mutationsList) {
    if (mutation.type === "childList") {
        chat.scrollTop = chat.scrollHeight;
    }
  }
};

const observer = new MutationObserver(callback);
observer.observe(chat, config);



// commented out section below is to test functionality

// let c = 0

// setInterval(function() {

//     const newElement = document.createElement("div")

//     // test for robot chat
//     newElement.className = 'd-flex align-items-end'

//     newElement.innerHTML = `<div class="chat-image-wrapper"><img src="blue-robot-mascot-logo-icon-design.png" alt="blue robot icon" class="rounded mx-2"></div><div class="d-flex justify-content-center align-items-center robot-text-wrapper"><p class="robot-text my-0"> ${format(c++, "Bottom position:", chat.scrollHeight - chat.clientHeight,  "Scroll position:", chat.scrollTop)}</p></div>`

//     chat.appendChild(newElement)

//     // test for user chat
//     // newElement.className = 'd-flex justify-content-end'

//     // newElement.innerHTML = `<div class="d-flex justify-content-center align-items-center user-text-wrapper"><p class="user-text my-0"> ${format(c++, "Bottom position:", chat.scrollHeight - chat.clientHeight,  "Scroll position:", chat.scrollTop)}</p></div>`

//     // chat.appendChild(newElement)

// }, 1000)

// function format () {
//     return Array.prototype.slice.call(arguments).join(' ')
// }