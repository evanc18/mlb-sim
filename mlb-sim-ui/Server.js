import express, { Express, Request, Response } from "express";

const app = express();

//Define port(s)
const port = process.env.PORT || 3000

//Config
const env = app.get('env')

// Serve static files
app.use(express.static('public'));
app.use(express.static('src'));

// Middleware
/**app.get('/', (req, res) => {
    res.sendFile('index.html');
});
*/


app.listen(port, () => {
  console.log('\n\033[1;33mStarted \033[0;32m' + env + '\033[1;33m environment\033[0m')
  console.log(`Server running on port ${port}...`);
  console.log('   [Ctrl + click] \x1b[4mhttp://localhost:' + port + '\n');
});