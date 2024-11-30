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
    pressed = false;
    console.log(pressed);
    document.querySelector('#cookies').style.display = 'none';
    setCookie("cookie-consent", false, 30);

    if (getCookie("theme")) {
        setCookie("theme", "", -1);
        console.log("Theme cookie removed");
    }
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
            // If there is no cookie-consent, show the consent banner
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
    function attachDeleteButtonListeners() {
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
    }

    function attachCloseButtonListeners() {
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
    }

    attachDeleteButtonListeners();
    attachCloseButtonListeners();


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

$(document).ready(function() {
    
    // Set the token so that we are not rejected by server 
    var csrf_token = $('meta[name=csrf-token]').attr('content'); 

    // Configure ajaxSetup so that the CSRF token is added to the header of every request 
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) { 
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) { 
                xhr.setRequestHeader("X-CSRFToken", csrf_token); 
            } 
        } 
    });  


    // $(document).on('click', '#post-open-modal-btn', function() {
    //     $('#post-confirmation-modal').css('display', 'block');
    // });

    // $(document).on('click', '#post-close-modal-btn', function() {

    //     $('#post-confirmation-modal').css('display', 'none');
    // });



    $(document).on("click", "a.vote", function() {
        var clicked_obj = $(this);  
        var post_id = $(this).attr('id'); 
        var vote_type = $(this).children()[0].id;  
        console.log("Vote button clicked for post ID: " + post_id + ", Vote type: " + vote_type);   
        
        $.ajax({ 
            url: '/vote', 
            type: 'POST', 
            data: JSON.stringify({ post_id: post_id, vote_type: vote_type}), 
            contentType: "application/json; charset=utf-8",         
            dataType: "json", 
            success: function(response){ 
                console.log(response);  
                // Update the html rendered to reflect new count 
                // Check which count to update 
                if(vote_type == "up") { 
                    clicked_obj.children()[1].innerHTML = " " + response.upvotes; 
                }

                var thumbsUpIcon = clicked_obj.find('i');
        
                // If the thumbs up icon as 'far' and is pressed, go from filled to unfilled or opposite
                if (thumbsUpIcon.hasClass('far')) {
                    thumbsUpIcon.removeClass('far').addClass('fas');
                } else {
                    thumbsUpIcon.removeClass('fas').addClass('far');
                }
            }, 
            error: function(error){ 
                console.log(error); 
            } 
        }); 
    }); 

    // load the users posts in this function
    function loadPosts(username) {
        $.ajax({
            // send data to this url, which is defined as a path in views.py
            url: '/profile/' + username + '/posts',
            type: 'GET',
            // #content-area is a div in profile.html, this is saying to add to #content-area whatever views path returns
            // it then makes the button of which were on active to look different
            success: function(response) {
                $('#content-area').html(response);
                $('#posts-btn').addClass('active');
                $('#likes-btn').removeClass('active');
                attachDeleteButtonListeners();
                attachCloseButtonListeners();
            },
            error: function(error) {
                console.log(error);
                $('#content-area').html('<p>Error loading posts</p>');
            }

        });
    }

    function loadLikes(username) {
        $.ajax({
            url: '/profile/' + username + '/likes',
            type: 'GET',
            success: function(response) {
                $('#content-area').html(response);
                $('#likes-btn').addClass('active');
                $('#posts-btn').removeClass('active');
                attachDeleteButtonListeners();
                attachCloseButtonListeners();
            },
            error: function(error) {
                console.log(error);
                $('#content-area').html('<p>Error loading liked posts</p>');
            }
        });
    }

    $('#posts-btn').on('click', function() {
        const username = $(this).data('username');
        loadPosts(username);
    });

    // if user presses like button, go to loadLikes function
    $('#likes-btn').on('click', function() {
        const username = $(this).data('username');
        loadLikes(username);
    });

    // makes posts appear straiht away as default
    const username = $('#posts-btn').data('username');
    if (username) {
        loadPosts(username);
    }

    // search bar functionality now
    $('#search_text').on("keyup", function() {
        let search_text = $(this).val().trim();
        
        // Make the request even if search is empty
        $.ajax({
            url: "/search/" + encodeURIComponent(search_text),
            type: 'GET',
            success: function(response) {
                $("#result").html(response);
                attachDeleteButtonListeners();
                attachCloseButtonListeners();
            },
            error: function(error) {
                console.log("Search error:", error);
                $("#result").html('<p>No results matching your search</p>');
            }

            
        });
    });
});



