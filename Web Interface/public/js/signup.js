/* Function that signs user up and is called when user clicks create account button */
function signup() {
  //Gets values from input
  username = document.getElementById("username").value;
  organization = document.getElementById("orgName").value;
	password = document.getElementById("password").value;
	passwordRep = document.getElementById("passwordRep").value;

	// Check if there are any empty fields
	if(orgName==null || username==null || password==null || passwordRep==null){
		document.getElementById("pwError").innerHTML = "Empty Fields";
	}
	// Checks if password is equal to repeat password
	else if(password!=passwordRep){
		document.getElementById("pwError").innerHTML = "Passwords do not match";
	}
	// Code to send account information to API
	else{
    $.ajax({
        url: '/signup',
        type: 'POST',
        data: {username: username, password: password, org: organization},
        success: function (data) {
          //Redirects to login page if there is no error
          if(!data.error) {
              window.location = "/login";
          } 
          //Puts error message on signup page
          else {
            document.getElementById("pwError").innerHTML = data.message;
          }
        },
        //Puts error in console
        error: function(err) {
          console.log(err);
        }
    });
	}
}
