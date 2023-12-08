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

document.addEventListener("DOMContentLoaded", function() {
    const chatIcon = document.getElementById('chatIcon');
    const controlIcon = document.getElementById('controlIcon');
    let interactionWrapper = document.getElementById('interactionWrapper');

    const chatIconSelected = './resources/chatIconSelected.png';
    const chatIconDeselected = './resources/chatIcon.png';
    const controlIconSelected = './resources/controllerIconSelected.png';
    const controlIconDeselected = './resources/controllerIcon.png';

    let chatSave;
    let controlSave;

    // Work in progress
    function reexecuteChatScript() {
        const oldScript = document.querySelector('#interactionWrapper script[src="function/chatUpdate.js"]');
        if (oldScript) {
            oldScript.remove();
        }
    
        const newScript = document.createElement("script");
        newScript.src = "function/chatUpdate.js";
        document.getElementById('interactionWrapper').appendChild(newScript);
    }

    async function loadContent(url, mode) {
        if (mode === "chat" && chatSave) {
            interactionWrapper.innerHTML = '';
            interactionWrapper.appendChild(chatSave.cloneNode(true));
            reexecuteChatScript();
            return;
        }
    
        if (mode === "control" && controlSave) {
            interactionWrapper.innerHTML = '';
            interactionWrapper.appendChild(controlSave.cloneNode(true));
            return;
        }

        const response = await fetch(url);
        if (response.ok) {
            const text = await response.text();
            interactionWrapper.innerHTML = text;

            if (mode === "chat") {
                chatSave = text;
            } else if (mode === "control") {
                controlSave = text;
            }

            Array.from(interactionWrapper.querySelectorAll("script")).forEach(oldScript => {
                const newScript = document.createElement("script");
                Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        } else {
            console.error(`Failed to load ${url}: ${response.statusText}`);
        }
    }

    chatIcon.src = chatIconSelected;
    loadContent('./iteractionModes/chatMode.html', "chat");

    chatIcon.addEventListener('click', function() {
        if (chatIcon.src.endsWith(chatIconSelected)) {
            chatSave = interactionWrapper.cloneNode(true);
            interactionWrapper.innerHTML = ''; 
            chatIcon.src = chatIconDeselected;
        } else {
            controlSave = interactionWrapper.cloneNode(true);
            chatIcon.src = chatIconSelected;
            controlIcon.src = controlIconDeselected;
            loadContent('./iteractionModes/chatMode.html', "chat");
        }
    });

    controlIcon.addEventListener('click', function() {
        if (controlIcon.src.endsWith(controlIconSelected)) {
            controlSave = interactionWrapper.cloneNode(true);
            interactionWrapper.innerHTML = ''; 
            controlIcon.src = controlIconDeselected;
        } else {
            chatSave = interactionWrapper.cloneNode(true);
            controlIcon.src = controlIconSelected;
            chatIcon.src = chatIconDeselected;
            loadContent('./iteractionModes/controlMode.html', "control");
        }
    });
});
