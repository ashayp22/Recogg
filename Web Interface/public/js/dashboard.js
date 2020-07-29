/* Performs code inside when page loads */
window.addEventListener('load', (event) => {
	//Hides loading messages
	document.getElementById("loadMsgNC").style.visibility = "hidden";
	document.getElementById("loadMsgDC").style.visibility = "hidden";

	//Updates dashboard with all of the classes
	updateClassroom();
});
/* Sets a cookie */
function setCookie(cname, cvalue, exdays) {
	//Creates a date object
	var d = new Date();
	//Sets time for date object
 	d.setTime(d.getTime() + (exdays*24*60*60*1000));
 	//Converts date object into a string
 	var expires = "expires="+ d.toUTCString();
 	//Creates a cookie
 	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
/* Creates class buttons on #classSection */
function createClass(name, uid, i) {
	//Creates a button element
	var button = document.createElement('button');
	//Sets the class of button to bootstrap class
	button.className = 'btn btn-default btn-lg org-class';
	//Styles button
	button.setAttribute('style', 'margin-top:2vw;margin-left:2vw;');
	//Assigns a hex color code to variable
	var randomColor = Math.floor(Math.random()*16777215).toString(16);
	//Styles button with the random color
	button.style.backgroundColor = "#" + randomColor;
	//Puts class name on the button
	button.textContent = name;
	//Sets id of the button to the uid parameter
	button.setAttribute('id', uid);
	/* Sets onclick to the button */
	button.onclick = function(e) {
		//Writes uid in the console
		console.log(this.id);
		//Creates a cookie with uid
		setCookie("uid", this.id);
		//Goes to classroom page
		window.location.href = "/classroom";
	};
	//Adds class button to #classSection
	document.getElementById('classSection').appendChild(button);
}
/* Updates dashboard with all the classes */
function updateClassroom() {
	//Writes "called" in console
	console.log("called")
	$.ajax({
        url: '/allClassrooms',
        type: 'POST',
        data: {},
        //Adds the loading animation when classes are loading onto dashboard
        beforeSend : function (){
				    $("#classSection").addClass("#preloader_img");
				  },
		//Front end gets all data needed
        success: function (data) {
			//Removes loading animation
			$("#classSection").removeClass("#preloader_img");
			//Assigns data from backend to variable
			body = data;
			//Clears #classSection before  adding on anything
			document.getElementById('classSection').innerHTML = ""
			//Classes are created if there is not error
			if (!body.error) {
				data = body.data;
				//Assigns array of certain color hex codes to variable
				colorArray = ['2D8AEB', 'EB2D3C', '2DEB32', 'CCED35', 'D72DEB']
				//Creates h1 element which will be added to #classSection as a header saying "classes"
				var tableMsg = document.createElement("H1")
				//Creates text node that says "classes"
				var h = document.createTextNode("Classes")
				//Adds the text node to the h1 element
				tableMsg.appendChild(h)
				//Alligns the text in the center of the h1 element
				tableMsg.setAttribute('style', 'text-align:center')
				//Adds the h1 element to #classSection
				document.getElementById("classSection").appendChild(tableMsg)
				//Creates a class button for each class that was in the body array
				var i = 0;
				for (var key in data) {
					createClass(data[key], key, i, colorArray[i % 6]);
					i++;
				}
			} 
			//Writes error message in console if there is an error in creating all the classes
			else {
				console.log(body.message)
			}
        },
        //Writes error message in the console if there is an error in getting data
        error: function(err) {
            console.log(err);
        }
    });
}
/* Creates a new class when user clicks on create class button */
function createNewClass(){
	//Shows loading message
	document.getElementById("loadMsgNC").style.visibility = "visible";

	//Assigns input value of name of class
	var className = document.getElementById("className").value;
	$.ajax({
        url: '/addClassroom',
        type: 'POST',
        data: {classroom: className},
        /* Disables user interaction until new class is fully loaded onto page */
        beforeSend: function () {
			//Adds no-click class from css/extra.css
	         $("main").addClass("no-click");			         
	    },
        success: function (data) {
        	//Writes classroom has been created if successful
			console.log(data);
			//Writes true if there is an error and false if successful
			console.log(data.error)

			//If there is no error the dashboard updates
			if (!data.error) {
				//Runs function to get and build all classes
				updateClassroom();

				//Hides the loading message
				document.getElementById("loadMsgNC").style.visibility = "hidden";

				//Enables user interaction
				$("main").removeClass("no-click");
			} 
			//Writes error message in console if there is an error
			else {
				console.log(data.message)
			}
        },
        //Puts error in console if there is an error
        error: function(err) {
            console.log(err);
        }
    });
}
/* Function gets cookie */
function getCookie(cname) {
	//Sets the cookie name to a variable
 	var name = cname + "=";
 	//Decodes cookie
	var decodedCookie = decodeURIComponent(document.cookie);
	//Splits the cookie with semicolons
	var ca = decodedCookie.split(';');
	//Returns necessary data from cookie
	for(var i = 0; i <ca.length; i++) {
 		var c = ca[i];
 		while (c.charAt(0) == ' ') {
    		c = c.substring(1);
		}
	    if (c.indexOf(name) == 0) {
	    	return c.substring(name.length, c.length);
	    }
  	}
	return "";
}
/* Deletes a class when user clicks on delete class button */
function deleteClass() {
	//Shows a loading message while class is being removed
	document.getElementById("loadMsgDC").style.visibility = "visible";

	//Puts each class into an array
	var elements = document.getElementsByClassName("org-class");
	//Assigns the name of the class to delete to variable
	var target = document.getElementById("classDel").value;
	//Creates blank uid variable
	var uid = ""

	//Assigns the class uid of the class to be deleted to uid by cycling through all classes
	for(var i = 0; i < elements.length; i++) {
		console.log(elements[i])
		if(elements[i].textContent == target) {
			uid = elements[i].id;
			break;
		}
	}

	//Ends the function if there is no class with the class name typed
	if (uid == "") {
		return;
	}

	$.ajax({
        url: '/deleteClass',
        type: 'POST',
        data: {uid: uid},
        //Disables user interaction until class is removed from page
        beforeSend: function () {
        	//Adds no-click class from css/extra.css
	        $("main").addClass("no-click");			         
	    },
        success: function (data) {
        	//Writes successfully deleted class if successful
			console.log(data);
			//Writes true if there is an error or false if there is no error
			console.log(data.error)
			if (!data.error) {
				//Adds all the classes to the dashboard
				updateClassroom();
				//Hides the loading message
				document.getElementById("loadMsgDC").style.visibility = "hidden";
				//Enables user interaction
				$("main").removeClass("no-click");
			}
			//Handles error
			else {
				
			}
        },
        //Writes error message in html if there is an error with retrieving data
        error: function(err) {
            document.getElementById('errorMessage').innerHTML = "Unable to delete class"
        }
    });
}