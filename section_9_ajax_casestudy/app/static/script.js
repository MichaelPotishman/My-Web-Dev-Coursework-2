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


document.addEventListener("DOMContentLoaded", function () {
    // POST DELETION!
    // each post has its own opening modal, confirming delete and close modal button so get ALL OF THEM
    const deleteButtons = document.querySelectorAll("#post-open-modal-btn");
    const modals = document.querySelectorAll("#post-confirmation-modal");
    const closeModalButtons = document.querySelectorAll("#post-close-modal-btn");

    // loop through the amount of delete buttons, changing the style fo the modals to show/hide them
    for (let i = 0; i < deleteButtons.length; i++) {
        deleteButtons[i].onclick = function() {
            modals[i].style.display = "flex";
        };

        closeModalButtons[i].onclick = function() {
            modals[i].style.display = "none";
        };
    }

    // Account Deletion Modal
    const accountDeleteBtn = document.getElementById("open-modal-btn");
    const accountModal = document.getElementById("account-confirmation-modal");
    const accountCloseBtn = document.getElementById("close-modal-btn");


    accountDeleteBtn.addEventListener("click", function() {
        accountModal.style.display = "flex";
    });


    accountCloseBtn.addEventListener("click", function() {
        accountModal.style.display = "none";
    });

    // Logout Modal
    const logoutBtn = document.getElementById("logout-open-modal-btn");
    const logoutModal = document.getElementById("logout-confirmation-modal");
    const logoutCloseBtn = document.getElementById("logout-close-modal-btn");


    logoutBtn.addEventListener("click", function() {
        logoutModal.style.display = "flex";

    });


    logoutCloseBtn.addEventListener("click", function() {
        logoutModal.style.display = "none";

    });
});



