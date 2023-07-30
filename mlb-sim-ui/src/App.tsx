import React from "react";
import { Component } from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, Router, RouterProvider, } from "react-router-dom";
import NavBar from "./components/NavBar";
import Login from "./components/Login";
import { Button, Container, Grid, Paper } from "@mui/material";
import './App.css';
import { auth } from "./Firebase";
//import splash from './src/assets/SplashScreen.png';

//TODO set an authentication state observer 

interface AppState {
    user?: any;
    page?: any;
}

export default class App extends Component<{}, AppState> {

    constructor(props: {}) {
        super(props);
        this.state = {
            user: auth.currentUser,
            page: null
        };
    }

    render() {
        if (!this.state.user && process.env.NODE_ENV !== 'development') {
            return (
                <div style={{
                    //backgroundImage: `url(${splash})`,
                    backgroundSize: 'cover',
                    height: '100%',
                    backgroundPosition: 'center',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    minHeight: '100vh'
                }}>
                    <Login onSignIn={user => this.setState({ user: user, page: null})} />
                </div>
            )
        } else {
            //const displayName = this.state.user.displayName;
            //const profilePhoto = this.state.user.photoURL;
            return (
                <div>
            <NavBar></NavBar>
            <Container maxWidth="lg" sx={{ mt:4, mb:4 }}>
            </Container></div>)
            
        }

    }
}