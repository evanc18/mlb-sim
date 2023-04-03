//TODO run server locally for debugging and feature testing
let port_ui = 4000;
let port_server = 5000;

let http = require('http')
let connect = require('connect');
const { platform } = require('os');
const express = require('express');

function createServer() {
    http.createServer(function(req, ses) {

    }).listen(port_server)
}

createServer()

let app = connect()
http.createServer(app).listen(port_ui);
console.log('Client listening on port ' + port_ui + '...');

const os = platform()
//const url = 'http://localhost:' + port_ui
//window.open(url)