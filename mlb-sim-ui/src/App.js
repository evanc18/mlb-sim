import React from "react";
//import { ajax } from "jquery";

class App extends React.Component {
    state = {
        user: undefined
    }

    async getGames() {

    }

    render() {

    }

    componentDidMount(){
        this.serverUrl = `http://${window.location.hostname}:5000`;
    }
}