/* Deletes account */
function deleteAccount() {
  $.ajax({
        url: '/deleteAccount',
        type: 'POST',
        data: {},
        success: function (data) {
                    //Writes message if successful in console
					console.log(data);
                    //Writes true if there is an error or false if successful in console
					console.log(data.error)
                    //Logs user out once account is deleted
					if (!data.error) {
						$("#logout").click();
					} 
                    else {

					}
        },
        //Writes error message if there is an error in deleting account
        error: function(err) {
            document.getElementById('errorMsg').innerHTML = "Unable to deleting account"
        }
    });
}
