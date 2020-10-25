# Recogg - Web Interface

<img src="screenshots/homepage.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

### Summary ###
Through the web interface of Recogg, users are able to create classrooms and add students. The interface gives users the ability to track the attendance of each classroom live and create a spreadsheet for the class.

### Features

* User Authentication
  * Secure User Sessions using Passport
  * Encrypted User Data using bcrypt
* Create/Remove Classrooms
  * Organizations can create classes
* Add/Remove Students & Employees
  * Organizations can add/remove students from the system
* Live Attendance Tracking
  * The interface provides live attendance tracking
* Download Attendance to Local Machine
  * Download spreadsheet with updated attendance of class
* Responsive Design (Web and Mobile Devices)
  * Web Interface works on Mobile Devices (iPhone, iPad, Android, Samsung) and on Computers (Windows, Mac, Linux)

### Architecture Diagram

<img src="screenshots/Web Interface.png" alt="diagram" style="float: left; margin-right: 10px;" />

### Built With
![Node.js](https://img.shields.io/badge/node-%3E%3D10.16.0-green)
![NPM](https://img.shields.io/badge/npm-%3E%3D6.9-orange)
![Bootstrap](https://img.shields.io/badge/bootstrap-%3E%3D4.0-red)
![HTML](https://img.shields.io/badge/HTML-5-yellowgreen)
![CSS](https://img.shields.io/badge/css-3-yellow)
![JavaScript](https://img.shields.io/badge/javascript-%3E%3D8-brightgreen)

* [Node.js](https://nodejs.org/en/)
* [Bootstrap](https://getbootstrap.com)
* [HTML/CSS/JavaScript/JQuery](https://html-css-js.com/)

## Getting Started

Follow along if you want to get the Web Interface running on your local machine.

### Prerequisites

In order to run the Web Interface locally, you must install:

* [Node.js](https://nodejs.org/en/download/)
* [NPM](https://www.npmjs.com/get-npm)


### Downloading to Local Machine

1. First, download the full [Web Interface folder](https://github.com/ashayp22/Recogg/tree/master/Web%20Interface). Then, unzip the folder to a secure location.
2. Next, open up the Command Line (Terminal or Command Prompt) and change the directory to match that of the web interface folder.
```
cd \...\Web Interface
```

### Running the Interface

In order to run the Web Interface, you must first download all of the dependencies listed in the package.json. Within the directory, type the following command:

```sh
npm install
```

Next, edit the .env file by adding in the API's endpoints. The endpoint should look like **https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/StageName/verifyaccount**.

```
VERIFY_ACCOUNT = ''
CREATE_ACCOUNT = ''
GET_CLASSROOMS = ''
CREATE_CLASSROOM = ''
GET_CLASSROOM_DATA = ''
UPLOAD_IMAGE = ''
NEW_MEETING = ''
GET_ATTENDANCE = ''
GET_UPDATE = ''
DELETE_ACCOUNT = ''
DELETE_CLASSROOM = ''
DELETE_STUDENT = ''
```

Next, type the following to run the web app locally:

```
node app.js
```

You will then be prompted to go to [http://localhost:3000/](http://localhost:3000/), which you should open up in their web browser.

## Usage

Once the user is in the web interface, they should click the button to get started:
<img src="screenshots/homepage.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

Once the user creates an account, they will be redirected to the dashboard. The dashboard will display all of the classrooms, but it starts off empty:
<img src="screenshots/dashboard-empty.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

To create a classroom, user can click on the create class button and enter the class name. After adding in a few classes, the page will look similar to this:
<img src="screenshots/dashboard-full.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

If a user wants to delete a class, they can simply click on the delete class button and type in the class name.

To enter the classroom, the user can click on the button corresponding to the class they want to enter. Once there, the page will initially look similar to this:
<img src="screenshots/class-empty.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

To add students to the class, the user can click the add student button and type in the student's name and upload the photo of the student's face. To remove a student, the user can click on the remove student button and type in the student's name. After adding in the students' names, the classroom will look similar to this:
<img src="screenshots/class-full.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

When it is time for a class to start, the teacher/administrator should click the new meeting button which will create a meeting corresponding to the current date. Then, the user should click the start tracking button. Once that happens, the user can track the attendance live; red means the student is not currently present, green means the student is currently present:
<img src="screenshots/class-red.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

Once the teacher wants to stop tracking the attendance, they can click on the stop tracking button.

If the teacher wants a spreadsheet on which there is the attendance of each date that there was a meeting created, they can click on the download attendance button. Once the teacher opens the downloaded file, the spreadsheet will look like this:
<img src="screenshots/spreadsheet.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />
If a student is present, there will be an "X" next to their name corresponding to each date there was a meeting. In the image above, no students were present.

If a user wants to delete an account, they can go to the account page, which is accessible from the top navigation bar. Once there, the user can click the delete organization button:
<img src="screenshots/account.JPG" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

Finally, all of the functionalities above can be done on a mobile device.


## More Information ##

For more information licenses, contributing, errors, and other components, visit the [front of the repository](https://github.com/ashayp22/Recogg).



