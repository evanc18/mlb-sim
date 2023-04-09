const express = require('express');

const app = express();

//Define port(s)
const port = process.env.PORT || 3000

//Config
const env = app.get('env')
console.log(env)

// Serve static files
app.use(express.static('public'));
app.use(express.static('src'));

// Serve the index.html file for all requests
app.get('/', (req, res) => {
    res.sendFile('index.html');
});


app.listen(port, () => {
  console.log(`Server running on port ${port}...`);
});