window.onload = function() {

    var buttonpressed;
    var buttonID;
    $('.Btn').click(function() {
        buttonpressed = $(this).attr('name')
        buttonID = $(this).attr('id')
        console.log(buttonID)
    })

    $('.QLike').on('submit', function(event){
        event.preventDefault();
        // console.log('button clicked was ' + buttonpressed)
        form = $(this).serialize();
        send(form, buttonpressed);
        buttonpressed=''
    });

    $('.ALike').on('submit', function(event){
        event.preventDefault();
        // console.log('button clicked was ' + buttonpressed)
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
                if (json == '403' || json == 'error') {
                    return false;
                } 
                console.log(json); // log the returned json to the console
                id = form.split('=')[1].toString();

                rating_id = buttonID[0] + 'rating_' + id;
                console.log(rating_id);
                $('#' + rating_id).text(json);

                if (buttonpressed == 'like') {
                    document.getElementById(buttonID).style.color = "green";
                    document.getElementById(buttonID[0] + "dis" + buttonID.slice(1, buttonID.length)).style.color = "initial";
                } else if (buttonpressed == 'dislike') {
                    document.getElementById(buttonID[0] + buttonID.slice(4, buttonID.length)).style.color = "initial";
                    document.getElementById(buttonID).style.color = "red";
                }
            }
        });
    }

    $("[id*=correct_]").click(function() {
        correct_id = $(this).attr('id');
        console.log(correct_id);
        // $(".correct_answer").remove();

        correct_send(correct_id);
    })

    function correct_send(correct_id) {
        // data['correct_id'] = correct_id;
        $.ajax({
            url : "/correct_answer/", // the endpoint
            type : "POST", // http method
            data: {'correct_id': correct_id},

            // handle a successful response
            success : function(json) {
                console.log(json);
                answer_id = "answer_" + correct_id.split('_')[1];
                console.log(answer_id);
                $(".correct_answer").remove();
                document.getElementById(answer_id).style.border = "2px solid green";
                document.getElementById(answer_id).style.borderBottom = "0px";
                document.getElementById(answer_id).style.borderTop = "0px";
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

}
