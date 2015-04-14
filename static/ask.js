answer = '<div class="alert alert-danger fade in" style="padding: 5px;"><button type="button" class="close close-alert" data-dismiss="alert" aria-hidden="true" style="height: 20px;">×</button>Enter '

function validateForm() {
    var inputTitle = document.forms["myForm"]["inputTitle"].value;
    var inputText = document.forms["myForm"]["inputText"].value;



    if (inputTitle == null || inputTitle == "") {
    	$( document ).ready(function() {
    		$('#message_inputTitle').html(answer + 'title</div>');
		});

		return false;	    	
    } else {
		$( document ).ready(function() {
    		$("#message_inputTitle").hide();
		});
    }

    if (inputText == null || inputText == "") {
    	$( document ).ready(function() {
    		$('#message_inputText').html(answer + 'text question</div>');
		});

		return false;	    	
    } else {
		$( document ).ready(function() {
    		$("#message_inputText").hide();
		});
    }
}