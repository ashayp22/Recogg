//Creates variable to check if user is tracking attendance (initially set to false)
var isTracking = false;

/* Performs code when page loads */
window.addEventListener('load', (event) => {
	//Hides loading messages when the page first loads
	document.getElementById("loadMsgAF").style.visibility = "hidden";
	document.getElementById("loadMsgRS").style.visibility = "hidden";
	document.getElementById("loadMsgFA").style.visibility = "hidden";

	//Displays class info and students
	reloadClass(true);
});

/* Updates classroom with all information */
function reloadClass(isFirst) {

	//a classroom hasn't been selected
	if(getCookie("uid") == "") {
		window.location.href = "/dashboard";
	}

	$.ajax({
		url: '/getClassData',
		type: 'POST',
		data: {uid: getCookie("uid")},
		//Adds preloader until page is fully updated
		beforeSend : function (){
		    $("#studNames").addClass("#preloader_img");
		},
		success: function (data) {
			//Removes preloader because information can get displayed
			$("#studNames").removeClass("#preloader_img");
			//Returns to dashboard if there is an error
			if (data.error) {
				window.location.href = "/dashboard";
			} 
			else {
				//Assigns date of last meeting to variable
				var alldata = data.data;
				console.log(data);
				console.log(alldata)
				var meetingCount = alldata.meeting_count;
				var name = alldata.name;
				var students = alldata.students;
				var lastDate = alldata.last_date;						
				//Assigns never to variable if there has never been a meeting
				if(lastDate === "") {
					lastDate = "Never";
				}

				//Writes when the last meeting was if user did not create a new meeting
				if(isFirst) {
					document.getElementById("dateDisplayed").innerHTML = "Last Meeting: " + lastDate + "<br>Number of Meetings: " + meetingCount;
				} 
				//Writes current meeting and date if user created a meeting
				else {
					document.getElementById("dateDisplayed").innerHTML = "Current Meeting: " + lastDate + "<br>Number of Meetings: " + meetingCount;
				}

				//Displays header information
				document.getElementById("spMessage").innerHTML = "Class Name: " + name
				document.getElementById("classUID").innerHTML = "Class UID: " + getCookie("uid")
				//Clears #studNames before adding any student names
				document.getElementById("studNames").innerHTML = ""

				//Creates h1 element which will be added to #classSection as a header saying "students"
				var tableMsg = document.createElement("H1")
				//Creates text node that says "students"
				var h = document.createTextNode("Students")
				//Adds the text node to the h1 element
				tableMsg.appendChild(h)
				//Alligns the text in the center of the h1 element and sets font size
				tableMsg.setAttribute('style', 'text-align:center;font-size:150%')
				//Adds the h1 element to #classSection
				document.getElementById("studNames").appendChild(tableMsg)

				//Creates a student for every name that was in the sudents array
				for(var i = 0; i < students.length; i++) {
					newStudent(students[i]);
				}

				//Updates #studNames every 5 seconds
				setTimeout(update, 5000);
			}
		},
		//Writes error message in console if there is an error
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
/* Sets all student divs to red because they are not initially present */
function setAllRed() {
	allStudents = document.getElementsByClassName("studentDiv");
	for(var i = 0; i < allStudents.length; i++) {
		allStudents[i].style.backgroundColor = "#FF0000";
	}
}
/* Checks if student is present */
function checkIn(arr, name) {
	//Returns true if student is in array of present students
	for(var i = 0; i < arr.length; i++) {
		if (arr[i] == name) {
			return true
		}
	}
	//Returns false if student is not in array of present students
	return false
}
/* Updates the color of each student div */
function updateAllStudents(goodStudents) {
	//Assigns all student divs to variable
	allStudents = document.getElementsByClassName("studentDiv");
	for(var i = 0; i < allStudents.length; i++) {
		//Sets student div to green if student is present
		if (checkIn(goodStudents, allStudents[i].id)) {
			allStudents[i].style.backgroundColor = "#00FF00";
		} 
		//Sets student div to red if student is not currently present
		else {
			allStudents[i].style.backgroundColor = "#FF0000";
		}
	}
}
/* Gets students that are present */
function getHere() {
	$.ajax({
		url: '/getUpdate',
		type: 'POST',
		data: {uid: getCookie("uid")},
		success: function (data) {
			//Assigns present students to variable
			goodStudents = data.students;

			//Changes color of each student that is present to green
			updateAllStudents(goodStudents);
		},
		//Writes error message in console if there is an error
		error: function(err) {
			console.log(err);
		}
	});
}
/* Resets all student divs to yellow */
function resetDivs() {
	allStudents = document.getElementsByClassName("studentDiv");
	for(var i = 0; i < allStudents.length; i++) {
		allStudents[i].style.backgroundColor = "#FFA500";
	}
}
/* Calls functions to update color of student div */
function update() {
	//Changes student div to green or red depending on if they are present or not
	if(isTracking) {
		getHere()
	}
	//Resets student div to yellow
	else {
		resetDivs()
	}
	//Calls update function every 30 seconds
	setTimeout(update, 30000);
}
/* Create a new student div */
function newStudent(name) {
	//Assigns #studNames to variable
	var div = document.getElementById("studNames");
	//Creates a div element
	var nameDiv = document.createElement('div');
	//Creates text node for the div
	className = document.createTextNode(name);
	//Adds text node to div
	nameDiv.appendChild(className);
	//Sets class for div
	nameDiv.className = 'studentDiv';
	//Sets id for div
	nameDiv.setAttribute('id', name);
	//Adds siv to student names section
	div.appendChild(nameDiv);
}
/* Updates student div */
function updateStudent(name, color) {
	//Gets every students div in array
	allStudents = document.getElementsByClassName("studentDiv");
	//Changes the color of each student div to color parameter
	for(var i = 0; i < allStudents.length; i++) {
		if (allStudents[i].id == name) {
			allStudents[i].style.backgroundColor = "#" + color;
			return;
		}
	}
}
/* Add student to class */
function addStudent() {
	//Shows loading message until student is added to page
	document.getElementById("loadMsgAF").style.visibility = "visible";

	//Assigns name of student to variable
	faceName = document.getElementById("faceName").value;
	//Assigns face image file to variable
	inputFiles = document.getElementById("faceImg").files;

	//Ends function if error with inputs
	if (faceName == "" || inputFiles[0] == null) {
		return;
	}

	//Creates new upload form
	var form = $('#fileUploadForm')[0];
	var data = new FormData(form);
	//Adds class uid to form
	data.append("uid", getCookie("uid"));
	$.ajax({
		url: '/addFace',
		type: 'POST',
		enctype: 'multipart/form-data',
		data: data,
		processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
        //Disables user interaction until student is added to page
        beforeSend: function () {
	         $("main").addClass("no-click");			         
	    },
		success: function (data) {
			//Writes error in console if there is an error
			if (data.error) {
				document.getElementById("fileMessage").innerHTML = data.message;
			} 
			//Adds student to page by reloading the page
			else {
				document.getElementById("fileMessage").innerHTML = data.message;
				reloadClass();
				//Enables user interaction
				$("main").removeClass("no-click");						
			}
			//Hides loading message because student is added to page
			document.getElementById("loadMsgAF").style.visibility = "hidden";
		},
		//Writes error message in console if there is an error
		error: function(err) {
			console.log(err);
		}
	});
}
/* Changes status of whether user is tracking attendance or not */
function changeTracking(){
	//Changes the tracking boolean
	isTracking = !isTracking;
	//Writes message in console
	console.log("changed tracking");
	//Changes button to allow user to stop attendance and calls function to change status of present students
	if(isTracking) {
		getHere();
		document.getElementById("trackingBtn").value = "Stop Attendance"
	} 
	//Changes button to allow user to start meeting and call function to reset the status of present students
	else {
		resetDivs();
		document.getElementById("trackingBtn").value = "Start Attendance"
	}
}
/* Creates new meeting */
function newMeeting(){
	//Shows loading message until meeting is fully created
	document.getElementById("loadMsgFA").style.visibility = "visible";

	//Create date object and format date object
	var today = new Date();
	var currentDate = (today.getMonth()+1)+'-'+today.getDate()+'-'+today.getFullYear();

	//Calls the api to increment the meeting count
	$.ajax({
		url: '/newMeeting',
		type: 'POST',
		data: {uid: getCookie("uid")},
		//Disables user interaction until meeting is fully created
		beforeSend: function () {
	         $("main").addClass("no-click");			         
	    },
		success: function (data) {
			//Displays message in console
			console.log(data);
			//Displays true in console if there is an error
			if (data.error) {
				console.log(data.error);
			} 
			//Calls function to reload the class
			else {
				reloadClass();
				//Enables user interaction
				$("main").removeClass("no-click");
				//Hides loading message because meeting has been fully created
				document.getElementById("loadMsgFA").style.visibility = "hidden";
			}
		},
		//Writes error message in console if there was an error
		error: function(err) {
			console.log(err);
		}
	});
}
/* Downloads spreadsheet with attendance on it */
function download() {
	//Shows loading message until file is downloaded
	document.getElementById("loadMsgFA").style.visibility = "visible";
	$.ajax({
		url: '/downloadAttendance',
		type: 'POST',
		data: {uid: getCookie("uid")},
		//Disbales user interaction
		beforeSend: function () {
	        $("main").addClass("no-click");			         
	    },
		success: function (data) {
			//Alerts if there was an error
			if (data.error) {
				alert(data.message);
			} 
			else {
				//Assigns csv file to variable
				var csvString = data.csv;
				var universalBOM = "\uFEFF";
				//Creates an a element
				var a = window.document.createElement('a');
				//Sets the link to csv file
				a.setAttribute('href', 'data:text/csv; charset=utf-8,' + encodeURIComponent(universalBOM+csvString));
				//Sets download attribute of link to download attendance.csv
				a.setAttribute('download', 'attendance.csv');
				//Adds attendance.csv to window
				window.document.body.appendChild(a);
				//Triggers click element
				a.click();

				//Enables user interaction
				$("main").removeClass("no-click");
				//Hides loading message becauase file is downloaded
				document.getElementById("loadMsgFA").style.visibility = "hidden";
			}
		},
		error: function(err) {
			console.log(err);
		}
	});
}
/* Removes student from classroom */
function deleteStudent() {
	//Shows loading message until student is removed from page
	document.getElementById("loadMsgRS").style.visibility = "visible";

	//Assigns name of student to be deleted to variable
	var student = document.getElementById("faceDel").value;

	//Ends function if input was empty
	if(student == "") {
		return;
	}
	$.ajax({
        url: '/deleteStudent',
        type: 'POST',
        data: {uid: getCookie("uid"), name: student},
        //Disables user interaction
        beforeSend: function () {
	        $("main").addClass("no-click");			         
	    },
        success: function (data) {
        	//Writes message in console if succesful
			console.log(data);
			//Writed true if there was an error and false if successful
			console.log(data.error)
			//Reloads class if successful
			if (!data.error) {
				reloadClass(true);
				//Hides loading message because student is removed from page
				document.getElementById("loadMsgRS").style.visibility = "hidden";
				//Enables user interaction
				$("main").removeClass("no-click");
			} 
			//Handles error
			else {
				
			}		
        },
        //Writes error message if there was an error
        error: function(err) {
            document.getElementById('errorMessage').innerHTML = "Unable to remove student"
        }
    });
}