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
document.querySelector('#all-cookies-btn').addEventListener('click', () => {
    pressed = true;
    console.log(pressed);
    document.querySelector('#cookies').style.display = 'none';
    setCookie("cookie-consent", true, 30);
})

document.querySelector('#mandatory-cookies-btn').addEventListener('click', () => {
    pressed = true;
    console.log(pressed);
    document.querySelector('#cookies').style.display = 'none';
    setCookie("cookie-consent", false, 30);
})

document.getElementById('manage-cookies').addEventListener('click', function () {
    document.querySelector('#cookies').style.display = 'block';
    setCookie("cookie-consent", false, 30);
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
    const deleteButtons = document.querySelectorAll('.right-buttons');

    for (let i = 0; i < deleteButtons.length; i++){
        deleteButtons[i].addEventListener("click", function () {
            const postID = deleteButtons[i].getAttribute("data-post-id");

            const modal = document.getElementById(`post-confirmation-modal-${postID}`);

            if (modal){
                modal.style.display = "block";
            }
        });

    }

    const closeModalButtons = document.querySelectorAll('.cancel-delete');
    
    for (let i = 0; i < closeModalButtons.length; i++){
        closeModalButtons[i].addEventListener("click", function () {
            const postID = closeModalButtons[i].getAttribute("data-post-id");

            const modal = document.getElementById(`post-confirmation-modal-${postID}`);

            if (modal){
                modal.style.display = "none";
            }
        });
    }


    // Account Deletion Modal
    const accountDeleteBtn = document.getElementById("open-modal-btn");
    const accountModal = document.getElementById("account-confirmation-modal");
    const accountCloseBtn = document.getElementById("close-modal-btn");

    const modalContainer = document.querySelector(".account-modal-container");


    accountDeleteBtn.addEventListener("click", function () {
        modalContainer.classList.add('active');
        accountModal.classList.add('active');
    });


    accountCloseBtn.addEventListener("click", function() {
        modalContainer.classList.remove('active');
        accountModal.classList.remove('active');
    });

    // Logout Modal
    const logoutBtn = document.getElementById("logout-open-modal-btn");
    const logoutModal = document.getElementById("logout-confirmation-modal");
    const logoutCloseBtn = document.getElementById("logout-close-modal-btn");

    const logoutModalContainer = document.querySelector(".logout-modal-container");


    logoutBtn.addEventListener("click", function() {
        logoutModalContainer.classList.add('active');
        logoutModal.classList.add('active');
    });


    logoutCloseBtn.addEventListener("click", function() {
        logoutModalContainer.classList.remove('active');
        logoutModal.classList.remove('active');

    });
});


