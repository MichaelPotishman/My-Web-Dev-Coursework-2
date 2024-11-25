const cookieConsent = getCookie("cookie-consent");

function setCookie(cookieName, cookieValue, expDays){
    let date = new Date();
    date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString()
    document.cookie = cookieName + "=" + cookieValue + ";" + expires + "; path=/";
}

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++){
        const cookie = cookies[i].split("=");
        if (cookie[0] === name){
            return cookie[1];
        }
    }
    return null;
}

// Get the button accepting cookies, once clicked change the div with id cookies to have diplay none (remove it)
// Then create a cookie called cookie-consent and set it to true and to expire in 30 days
let pressed = false;
document.querySelector('#cookies-btn').addEventListener('click', () => {
    pressed = true;
    console.log(pressed);
    document.querySelector('#cookies').style.display = 'none';
    setCookie("cookie-consent", true, 30);
})

document.addEventListener('DOMContentLoaded', function() {
    window.onload = function () {
        
        const themeCookie = getCookie("theme");

        // If the cookie exists and is set to true, hide the consent banner
        if (cookieConsent) {
            document.querySelector('#cookies').style.display = 'none'; // Hide the banner
        } else {
            // If no cookie, show the consent banner
            document.querySelector('#cookies').style.display = 'block';
        }
        

        if (themeCookie){
            if (themeCookie === 'dark'){
                document.body.classList.add('dark-theme');
                
            } else {
                document.body.classList.remove('dark-theme');
            }
        }
    }
})

document.getElementById('theme-toggle').addEventListener('click', function () {
    // Check if the body has the dark theme applied
    
    const themeOutput = document.getElementById("theme-toggle");
    if (document.body.classList.contains('dark-theme')) {
        // Switch to light mode
        document.body.classList.remove('dark-theme');
        themeOutput.innerText = 'Switch to Dark mode';
        
    } else {
        // Switch to dark mode
        document.body.classList.add('dark-theme');
        themeOutput.innerText = 'Switch to Light mode';
    }

    // Set a cookie to remember the user's theme preference for 365 days
    const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
    if (cookieConsent === 'true' || pressed){
        setCookie('theme', currentTheme, 365);
    }
    
});

// changing the icon of the thumbs up button
const voteButtons = document.querySelectorAll('.vote')

voteButtons.forEach(button => {
    button.addEventListener('click', function() {
        const icon = button.querySelector('i');

        if (icon.classList.contains('far')){
            icon.classList.remove('far');
            icon.classList.add('fas');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
        }
    })
})

// open modals for deleting account
document.addEventListener("DOMContentLoaded", function () {
    const openModalbtn = document.getElementById("open-modal-btn");
    const closeModalbtn = document.getElementById("close-modal-btn");
    const modal = document.getElementById("confirmation-modal");

    // show the modal when delete button pressed
    openModalbtn.addEventListener("click", function () {
        modal.style.display = "flex";
    });

    closeModalbtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    
});