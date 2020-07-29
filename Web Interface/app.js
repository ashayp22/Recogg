//all of the modules
const PORT = process.env.PORT || 3000; //either heroku port or local port
const express = require('express'); //routing
const bodyParser = require('body-parser'); //parsing requests
const app = express() //routing
const request = require('request'); //sending requests
const bcrypt = require('bcrypt'); //encrypting data
const passport = require('passport'); //user sessions
const flash = require('express-flash'); //user sessions
const session = require("express-session"); //user sessions
const methodOverride = require('method-override'); //overriding methods like DELETE
const formidable = require('formidable'); //form data
var fs = require('fs'); //file streams
require('dotenv').config(); //env file

const initializePassport = require('./passport-config'); //initialize reference to other node.js file

//returns user data, password, organization, based on the username
function getUser(username) {
  return new Promise((resolve, reject) => {
      var options = {
        'method': 'POST',
        'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/verifyaccount', //endpoint of verifying account
        'headers': {
        },
        formData: {
          'Account': JSON.stringify({"username": username}) //pass in username
        }
      };
      request(options, function (error, response) {
        body = JSON.parse(response["body"])
        if (body["error"]) { //error
          resolve(null);
        } else {
          resolve({username: body["username"], password: body["password"], organization: body["organization"]}) //resolve the Promise
        }
      });
    });
}


initializePassport(passport, async username => { //initializes passport
  //return the user in dictionary format with the username
  try {
    user = await getUser(username);
    return user;
  } catch (e) {
    console.log(e);
    return null;
  }
});

//all of the uses
app.use(express.static('public')); //public content directoru
app.use(bodyParser.json()); //body parser for json data
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.use(flash())
app.use(session({ //for sessions
  secret: process.env.SESSION_SECRET, //secret key
  resave: false,
  saveUninitialized: false
}))

//for the session
app.use(passport.initialize())
app.use(passport.session())
app.use(methodOverride('_method'))

//render the home page
app.get('/', (req, res) => {
  res.render('home');
})

//render the account page
app.get('/account', function (req, res) {
  res.render('account', {name: req.user.organization, msg: ""});
})

//render the home page
app.get('/home', (req, res) => {
  res.render('home');
})

//render the login page
app.get('/login', checkNotAuthenticated, (req, res) => { 
  console.log("rendering login")
  res.render('login', {msg: ""});
})

//login failed redirect
app.get('/loginFailed', checkNotAuthenticated, (req, res) => {
  res.render('login', {msg: 'Invalid login credentials'});
})

//post request - user trys to login 
app.post('/login', checkNotAuthenticated, passport.authenticate('local', {
  successRedirect: '/dashboard', //success, redirect to dashboard
  failureRedirect: '/loginFailed', //failed, redirect to login again
  failureFlash: true
}))


//render the signup page
app.get('/signup', checkNotAuthenticated, (req, res) => { 
  res.render('signup');
})

//user trys signing up
app.post('/signup', checkNotAuthenticated, async (req, res) => { 

  //get the data
  const username = req.body.username;
  const password = req.body.password;
  const org = req.body.org;

  if (username.length >= 4 && password.length >= 4) { //make sure the data is the correct length

      try {
        const hashedPassword = await bcrypt.hash(password, 10); //encrypt the password

        var options = {
        'method': 'POST',
        'url': "https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/createaccount", //endpoint for creating an account
        'headers': {
        },
        formData: {
          'Account': JSON.stringify({"username": username, "password": hashedPassword, "organization": org}) //body data
        }
        };

        request(options, function (error, response) {
          if (error) throw new Error(error);
          body = JSON.parse(response["body"])
          res.json({error: body["error"], message: body["message"]}) //return the response from the API
          res.end();
        });

      } catch {
        res.json({error: true, message: "Error, please try again."}); 
      }
  } else {
    res.json({error: true, message: "Your username and password is too short, please try again."}); //bad message
  }

})

//DELETE - log out user
app.delete('/logout', (req, res) => {
    req.logOut();
    res.redirect('/');
})

//render dashboard
app.get('/dashboard', checkAuthenticated, (req, res) => { 
  console.log("going to dashboard")
  res.render('dashboard', {name: req.user.organization});
})

//middleware - continue if a user is logged in
function checkAuthenticated(req, res, next) {
  console.log("checking if authenticated");
  if (req.isAuthenticated()) {
    return next()
  }
  res.redirect('/login')
}

//middleware - continue if a user is not logged in
function checkNotAuthenticated(req, res, next) {
  console.log("checking if not authenticated");
  if (req.isAuthenticated()) {
    return res.redirect('/dashboard')
  }
  next()
}

app.post('/allClassrooms', checkAuthenticated, (req, res) => {
  console.log(req.user.username)
  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/getclassrooms', //endpoint for getting classrooms associated with the user account
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"username": req.user.username}) //pass in the username
    }
  };

  request(options, function (error, response) {
    body = JSON.parse(response["body"])
    if (body["error"]) { //if there is an error, send back the message
      res.json({error: body["error"], message: body["message"]})
      res.end();
    } else { //send the data
      console.log(body);
      res.json({error: body["error"], data: body["data"]})
      res.end();
    }
  });
})

//adding a classroom
app.post('/addClassroom', checkAuthenticated, (req, res) => { 
  var name = req.body.classroom;
  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/createclassroom', //endpoint for creating a classroom
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"username": req.user.username, "password": req.user.password, "classroom": name}) //data that is passed
    }
  };
  request(options, function (error, response) {
    body = JSON.parse(response["body"])
    res.json({error: body["error"], message: body["message"]})
    res.end();
  });
})


//rendering the classroom page
app.get('/classroom', checkAuthenticated, (req, res) => {
  res.render('class');
})

//gets all of the data for a class
app.post('/getClassData', checkAuthenticated, (req, res) => { 

  var uid = req.body.uid;

  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/getclassroomdata', //endpoint for getting classroom data
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"uid": uid}) //uid is passed
    }
  };
  request(options, function (error, response) {
    body = JSON.parse(response["body"])

    if(body["error"]) { //error
      res.json({error: body["error"], message: body["message"]}) //send back the message
      res.end();
    } else {
      var data = body["data"];
      res.json({error: false, data: data}) //send the data for the classroom
      res.end();
    }
  });
})

//adds a students face
app.post('/addFace', checkAuthenticated, (req, res) => { 

  var form = new formidable.IncomingForm(); //incoming multipart request
    form.parse(req, function (err, fields, files) {

      //get data
      var uid = fields.uid; //string
      var name = fields.faceName; //string
      var image = files.studentImage; //image

      //upload image
      var options = {
        'method': 'POST',
        'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/uploadimage', //endpoint
        'headers': {
        },
        formData: {
          'file': {
            'value': fs.createReadStream(image.path), //read the file which is temporaily saved
            'options': {
              'filename': image.name,
              'contentType': null
            }
          },
          'Metadata': JSON.stringify({uid: uid, filename: "student.jpg", label: name}) //send data
        }
      };
      request(options, function (error, response) {
        body = JSON.parse(response["body"])
        console.log(body)
        res.json({error: body["error"], message: body["message"]}) //return the response from the API
        res.end();
      });
    })

})


//start a new meeting
app.post('/newMeeting', checkAuthenticated, (req, res) => { 
  var uid = req.body.uid;

  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/newmeeting', //endpoint for new meeting
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"uid": uid}) //pass in uid
    }
  };
  request(options, function (error, response) {
    body = JSON.parse(response["body"])
    res.json({error: body["error"], message: body["message"]})
    res.end();
  });
})

//downloading the attendance (csv file)
app.post('/downloadAttendance', checkAuthenticated, (req, res) => { 
  var uid = req.body.uid;

  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/getattendance', //endpoint for getting the attendance
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"uid": uid})
    }
  };
  request(options, function (error, response) {
    if(error) {
      res.json({error: true, message: "error, please try again"})
      res.end();
    } else {
      res.json({error: false, csv: response["body"]}) //return the csv file
      res.end();
    }
  });
})

//getting an update for students in the current meeting
app.post('/getUpdate', checkAuthenticated, (req, res) => { 
  var uid = req.body.uid;

  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/getupdate', //get update endpoint
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"uid": uid})
    }
  };
  request(options, function (error, response) {
    body = JSON.parse(response["body"])
    if(error) {
      res.json({error: true, message: "error, please try again"}) //return a message if there is an error
      res.end();
    } else {
      res.json({error: false, students: body["students"]}) //return the students present
      res.end();
    }
  });
})

//delete an account
app.post('/deleteAccount', checkAuthenticated, (req, res) => { 
  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/deleteaccount', //delete account
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"username": req.user.username, "password": req.user.password}) //user data
    }
  };
  request(options, function (error, response) {
    body = JSON.parse(response["body"])
    res.json({error: body["error"], message: body["message"]})
    res.end();
  });
})

//delete a class
app.post('/deleteClass', checkAuthenticated, (req, res) => {

  var uid = req.body.uid;

  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/deleteclassroom', //deletes a classroom
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"username": req.user.username, "password": req.user.password, "uid": uid}) //data passed in
    }
  };
  request(options, function (error, response) {
    body = JSON.parse(response["body"])
    res.json({error: body["error"], message: body["message"]}) //return the API response
    res.end();
  });
})

//delete a student associated to a specific class
app.post('/deleteStudent', checkAuthenticated, (req, res) => { //handles get request

  var uid = req.body.uid;
  var name = req.body.name;

  var options = {
    'method': 'POST',
    'url': 'https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/deletestudent', //delete student endpoint
    'headers': {
    },
    formData: {
      'Account': JSON.stringify({"name": name, "uid": uid}) //data passed
    }
  };
  request(options, function (error, response) {
    body = JSON.parse(response["body"])
    res.json({error: body["error"], message: body["message"]}) //return the response from the API
    res.end();
  });
})

//starting up a local server
app.listen(PORT, function () {
  console.log('go to http://localhost:3000/')
})
