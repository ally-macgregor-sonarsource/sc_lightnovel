const express = require('express');
const mogan = require('morgan');
const app = express();
const PORT = 4200;
const accessToken = process.env.TOKEN;

// expose as function for testing
module.exports = app;

app.get('/', (req, res) => {
    var whoIsIt = req.headers['special_knock'];
    console.log('Secret passcode is ' + accessToken);
    console.log('Knock Knock, it is ' + whoIsIt);

    if (whoIsIt === accessToken)
    {
        res.json({ message: 'Hello ' + whoIsIt});    
    }
    else
    {
        res.status(401);
        res.json({ message: 'You are not welcomed here!'});
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    
    // Left here intentionally to see what SCM tools will catch it.
    console.log('Secret passcode or password is ' + accessToken);
    console.log('Secret passcode or password is '+ 'my_password');
   
   var passcode = 'my_sensitive_password';
});
