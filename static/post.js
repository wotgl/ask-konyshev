window.onload = function() {
    $('#post-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_post();
    });

    // $('.QLike').on('submit', function(event){
    //     event.preventDefault();
    //     console.log("form submitted!")  // sanity check
    //     //create_post();

    // });

    var buttonpressed;
    $('.QBtn').click(function() {
        buttonpressed = $(this).attr('name')
    })

    $('.QLike').on('submit', function(event){
        event.preventDefault();
        console.log('button clicked was ' + buttonpressed)
        form = $(this).serialize();

        send(form, buttonpressed);

        buttonpressed=''
    });


    function send(form, buttonpressed) {
        data = {};
        data['form'] = form;
        data['buttonpressed'] = buttonpressed;
        $.ajax({
            url : "/like/", // the endpoint
            type : "POST", // http method
            data: data,

            // handle a successful response
            success : function(json) {
                console.log(json); // log the returned json to the console
                id = form.split('=')[1].toString();
                rating_id = 'rating_' + id;
                console.log(rating_id)
                $('#' + rating_id).text(json);

                if (buttonpressed == 'like') {
                    document.getElementById("likeBtn_" + id).style.color = "green";
                    document.getElementById("dislikeBtn_" + id).style.color = "initial";
                } else if (buttonpressed == 'dislike') {
                    document.getElementById("likeBtn_" + id).style.color = "initial";
                    document.getElementById("dislikeBtn_" + id).style.color = "red";
                }
            }
        });
    }


    $.ajaxSetup({ 
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
             }

             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         } 
    });

    function create_post() {
        console.log("create post is working!") // sanity check
        $.ajax({
            url : "create_post/", // the endpoint
            type : "POST", // http method
            data : { the_post : $('#post-text').val() }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };
}
