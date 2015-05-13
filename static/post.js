window.onload = function() {

    $("[id*=QlikeBtn_]").click(function() {
        button_id = $(this).attr('id');
        send(button_id, 'like');

        return false;
    })

    $("[id*=QdislikeBtn_]").click(function() {
        button_id = $(this).attr('id');
        send(button_id, 'dislike');

        return false;
    })

    $("[id*=AlikeBtn_]").click(function() {
        button_id = $(this).attr('id');
        console.log('AlikeBtn_');
        send(button_id, 'like');

        return false;
    })

    $("[id*=AdislikeBtn_]").click(function() {
        button_id = $(this).attr('id');
        console.log('AdislikeBtn_');
        send(button_id, 'dislike');

        return false;
    })

    // $("[id*=dislikeBtn_]").click(function() {
    //     button_id = $(this).attr('id');
    //     console.log(button_id)
    //     send(button_id, 'dislike');

    //     return false;
    // })
    // $("[id*=likeBtn_]").click(function() {
    //     button_id = $(this).attr('id');
    //     console.log(button_id)
    //     send(button_id, 'like');

    //     return false;
    // })

    

    function send(button_id, state) {
        data = {};
        data['button'] = button_id;
        data['state'] = state;
        $.ajax({
            url : "/like/", // the endpoint
            type : "POST", // http method
            data: data,

            // handle a successful response
            success : function(json) {
                console.log(json);
                
                if (json == '403' || json == 'error' || json == 'value exist') {
                    return false;
                } 
                // var re = /^\d+$/
                // if (!re.test(json)) {
                //     console.log('catch');
                //     return false;
                // }

                rating_id = button_id[0] + 'rating_' + button_id.split('_')[1];
                // console.log(rating_id);
                $('#' + rating_id).text(json);

                if (state == 'like') {
                    document.getElementById(button_id).style.color = "green";
                    // document.getElementById(button_id).setAttribute("disabled", "true");
                    document.getElementById(button_id[0] + "dis" + button_id.slice(1, button_id.length)).style.color = "initial";
                    // document.getElementById(button_id[0] + "dis" + button_id.slice(1, button_id.length)).setAttribute("disabled", "true");
                } else if (state == 'dislike') {
                    document.getElementById(button_id[0] + button_id.slice(4, button_id.length)).style.color = "initial";
                    // document.getElementById(button_id[0] + button_id.slice(4, button_id.length)).setAttribute("disabled", "true");
                    document.getElementById(button_id).style.color = "red";
                    // document.getElementById(button_id).setAttribute("disabled", "true");
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
                if (json == '403' || json == 'error' || json == 'value exist') {
                    return false;
                } 
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
