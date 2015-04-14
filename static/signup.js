answer = '<div class="alert alert-danger fade in" style="padding: 5px;"><button type="button" class="close close-alert" data-dismiss="alert" aria-hidden="true" style="height: 20px;">×</button>Enter '

function validateForm() {
    var inputName = document.forms["myForm"]["inputName"].value;
    var inputEmail = document.forms["myForm"]["inputEmail"].value;
    var inputPassword = document.forms["myForm"]["inputPassword"].value;
    var inputUsername = document.forms["myForm"]["inputUsername"].value;



    if (inputName == null || inputName == "") {
    	$( document ).ready(function() {
    		$('#message_inputName').html(answer + 'name</div>');
		});

		return false;	    	
    } else {
		$( document ).ready(function() {
    		$("#message_inputName").hide();
		});
    }

    if (inputEmail == null || inputEmail == "") {
		$( document ).ready(function() {
			$('#message_inputEmail').html(answer + 'email</div>');
		});

		return false;	    	
    } else {
    	var at_sign = inputEmail.indexOf('@');
    	var dot_sign = inputEmail.indexOf('.');
    	if ((dot_sign - at_sign > 1) && at_sign > 0) {
    		$( document ).ready(function() {
    			$("#message_inputEmail").hide();
			});
    	} else return false;
    }

    if (inputPassword == null || inputPassword == "") {
    	$( document ).ready(function() {
			$('#message_inputPassword').html(answer + 'password</div>');		
		});

		return false;	    	
    } else {
    	$( document ).ready(function() {
    		$("#message_inputPassword").hide();
		});
    }

    if (inputUsername == null || inputUsername == "") {
    	$( document ).ready(function() {
			$('#message_inputUsername').html(answer + 'username</div>');		
		});

		return false;	    	
    } else {
    	$( document ).ready(function() {
    		$("#message_inputUsername").hide();
		});
    }

    
}