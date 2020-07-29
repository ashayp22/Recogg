const LocalStrategy = require('passport-local').Strategy; //local strategy for passport module
const bcrypt = require("bcrypt"); //for encryption

function initialize(passport, getUser) { //initialize method
  passport.use(new LocalStrategy( async function (username, password, done) {
    const user = await getUser(username) //first, get the user
      if (user == null) { //user doesn't exist
        console.log("no user exists")
        return done(null, false)
      }
      //now that we have the user, we will check to see if the user is authenticated
      try {
        if (await bcrypt.compare(password, user.password)) {
          console.log("correct password");
            return done(null, user); //good user
        } else {
          console.log("incorrect password")
          return done(null,false) //bad user
        }
      } catch (e) {
        console.log(e)
        return done(null, false);
      }
  }));

  passport.serializeUser((user, done) =>  { //serializes user
    console.log("serializing")
    return done(null, user.username)
  })
  passport.deserializeUser(async (username, done) => { //deserializes user, used for getting user data
    console.log('deserializing');
    return done(null, await getUser(username))
  })
}


module.exports = initialize //allow the initialize method to be exported
