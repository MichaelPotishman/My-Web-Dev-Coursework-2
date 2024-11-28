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
            },
            error: function(error) {
                console.log("Search error:", error);
                $("#result").html('<p>No results matching your search</p>');
            }
        });
    });
});


    // $('#search_text').keyup(function(){
    //     var search = $(this).val();
        
    //     if (search.trim() !== ''){
    //         $.ajax({
    //             url: "/livesearch",
    //             method: "POST",
    //             data: {query: search},
    //             success: function(data) {
    //                 $('.bottom-container').html(data);
    //             }
    //         });
    //     } else {
    //         // Reload all posts when search is empty
    //         location.reload();
    //     }
    // });