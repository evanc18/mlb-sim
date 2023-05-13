import React from "react";
import { Component } from "react";
import NavBar from "./components/NavBar";
import Login from "./components/Login";
import { Container } from "@mui/material";
import './App.css';
import { auth } from "./Firebase";
import splash from './assets/SplashScreen.png';

//TODO set an authentication state observer 

interface AppState {
    user?: any;
}

export default class App extends Component<{}, AppState> {

    constructor(props: {}) {
        super(props);
        this.state = {
            user: auth.currentUser
        };
    }

    render() {
        if (!this.state.user && process.env.NODE_ENV !== 'development') {
            return (
                <div style={{
                    backgroundImage: `url(${splash})`,
                    backgroundSize: 'cover',
                    height: '100%',
                    backgroundPosition: 'center',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    minHeight: '100vh'
                }}>
                    <Login onSignIn={user => this.setState({ user })} />
                </div>
            )
        } else {
            //const displayName = this.state.user.displayName;
            //const profilePhoto = this.state.user.photoURL;
            return <NavBar></NavBar>
        }

    }
}