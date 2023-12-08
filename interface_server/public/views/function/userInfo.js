let usersName;

function getUserInformation() {
    // Check if a name cookie already exists
    usersName = getCookie("username");
  
    if (usersName) {
      alert("Welcome back " + usersName + "!");
    } else {
        usersName = prompt("Please enter your name:", "");
  
      if (usersName != null && usersName != "") {
        saveCookie("username", usersName)
        alert("Welcome " + usersName + "!");
      } else {
        alert("Welcome, guest!");
      }
    }
  }
  
  function saveCookie(varName, varValue) {
    var daysToExpire = 7;
    var date = new Date();
    date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
    var expires = "expires=" + date.toUTCString();
    document.cookie = varName + "=" + varValue + ";" + expires + ";path=/";
  }

  // Function to retrieve a cookie by name
  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

// Only add the event listener after the window has loaded.
document.addEventListener('DOMContentLoaded', (event) => {
    console.log("hello friends");

    getUserInformation();
});