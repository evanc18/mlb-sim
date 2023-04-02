//TODO run server locally for debugging and feature testing
let port_ui = 3000;
let port_server = 5000;

let http = require('http')
let connect = require('connect')


function createServer() {
    http.createServer(function(req, ses) {

    }).listen(port_server)
}

createServer()

let app = connect()
http.createServer(app).listen(uiPort);
console.log('Client listening on port ' + uiPort + '...');