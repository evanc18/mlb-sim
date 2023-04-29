import { Grid, TextField, Button, Typography, Link, Paper, Container, Alert } from "@mui/material";
import { auth, firestore } from '../Firebase';
import { sendPasswordResetEmail, signInWithEmailAndPassword, createUserWithEmailAndPassword, UserCredential } from "firebase/auth";
import { Fragment, useEffect, useState } from "react";

interface LoginProps {
    onSignIn: (user: any) => void;
}

interface LoginState {
    username: string;
    password: string;
    confirmPassword: string;
    errorAlert: { visible: boolean, type: any, text: string };
    mode: string;
}

const Login = ({ onSignIn }: LoginProps) => {

    const [state, setState] = useState<LoginState>({
        username: '',
        password: '',
        confirmPassword: '',
        errorAlert: { visible: false, type: 'error', text: '' },
        mode: 'sign-in'
    });



    const handleSubmit = (event) => {
        event.preventDefault();
        if (state.mode === 'sign-in') {
            handleSignIn();
        } else if (state.mode === 'create-account') {
            handleSignUp();
        } else if (state.mode === 'reset-password') {
            handlePasswordReset();
        }
    }

    const handleSignIn = () => {
        signInWithEmailAndPassword(auth, state.username, state.password)
            .then(
                (userCredential: UserCredential) => {
                    const user = userCredential.user;
                    console.log(`Signed in as ${user.email}`);
                    onSignIn(user);
                })
            .catch(error => {
                let message = 'Fatal! firebase/auth error in login of user'
                if (error.code === 'auth/user-disabled') {
                    message = 'Email has been disabled.';
                } else if (error.code === 'auth/invalid-email') {
                    message = 'Please enter a valid email address.'
                } else if (error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
                    message = 'Email or password incorrect.'
                }
                setState({
                    ...state, errorAlert: {
                        visible: true,
                        type: 'error',
                        text: message
                    }
                });
            });
    }

    const handleSignUp = () => {
        if (state.password === state.confirmPassword) {
            createUserWithEmailAndPassword(auth, state.username, state.password)
                .then(
                    (userCredential: UserCredential) => {
                        const user = userCredential.user;
                        console.log(`Signed up as ${user.email}`);
                        onSignIn(user);
                    })
                .catch(error => {
                    let message = 'Fatal! firebase/auth error in creation of user'
                    if (error.code === 'auth/email-already-in-use') {
                        message = 'Email already in use!';
                    } else if (error.code === 'auth/invalid-email') {
                        message = 'Please enter a valid email address.'
                    } else if (error.code === 'auth/weak-password') {
                        message = 'Weak password! Please use atleast 6 characters'
                    }
                    setState({
                        ...state, errorAlert: {
                            visible: true,
                            type: 'error',
                            text: message
                        }
                    })
                });
        }
    }

    const handlePasswordReset = () => {
        //Change grid to password reset mode
        sendPasswordResetEmail(auth, state.username)
            .then(() =>
                setState({
                    ...state, errorAlert: {
                        visible: true,
                        type: 'success',
                        text: 'Password reset email sent!'
                    }
                })
            )
            .catch(error => {
                let message = 'Fatal! firebase/auth error in password reset of user'
                if (error.code === 'auth/user-not-found') {
                    message = 'No users found for this email!';
                } else if (error.code === 'auth/invalid-email') {
                    message = 'Please enter a valid email address.'
                }
                setState({
                    ...state, errorAlert: {
                        visible: true,
                        type: 'error',
                        text: message
                    }
                });
            });
    }

    let annotation;
    let errorAlertElement = <Grid item xs={12}><Alert severity={state.errorAlert.type}>{state.errorAlert.text}</Alert></Grid>;

    if (state.mode === 'create-account') {
        annotation =
            <Fragment>
                <Grid item xs={12}>
                    <TextField
                        label="Email"
                        variant="outlined"
                        fullWidth
                        required
                        value={state.username}
                        onChange={(event) => setState({ ...state, username: event.target.value })}
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        label="Password"
                        variant="outlined"
                        type="password"
                        fullWidth
                        required
                        value={state.password}
                        onChange={(event) => setState({ ...state, password: event.target.value })}
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        label="Confirm Password"
                        variant="outlined"
                        type="password"
                        fullWidth
                        required
                        value={state.confirmPassword}
                        error={state.confirmPassword !== state.password ? true : false}
                        onChange={(event) => setState({ ...state, confirmPassword: event.target.value })}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Button variant="contained" color="secondary" fullWidth type="submit">
                        Sign Up
                    </Button>
                </Grid>
                <Grid item xs={12}>
                    <Typography align="center" variant="subtitle2">
                        <Link
                            onClick={() => { setState({ ...state, password: '', mode: 'sign-in', errorAlert: { visible: false, type: 'error', text: '' } }) }}
                            style={{ cursor: "pointer" }}
                        >
                            Back
                        </Link>
                    </Typography>
                </Grid>
            </Fragment>
    } else if (state.mode === 'reset-password') {
        annotation =
            <Fragment>
                <Grid item xs={12}>
                    <TextField
                        label="Email"
                        variant="outlined"
                        fullWidth
                        required
                        value={state.username}
                        onChange={(event) => setState({ ...state, username: event.target.value })}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Button variant="contained" color="secondary" fullWidth type="submit">
                        Send Reset Email
                    </Button>
                </Grid>
                <Grid item xs={12}>
                    <Typography align="center" variant="subtitle2">
                        <Link
                            onClick={() => setState({ ...state, password: '', mode: 'sign-in', errorAlert: { visible: false, type: 'error', text: '' } })} // Add your own click handler here
                            style={{ cursor: "pointer" }}
                        >
                            Back
                        </Link>
                    </Typography>
                </Grid>
            </Fragment>
    } else {
        annotation =
            <Fragment>
                <Grid item xs={12}>
                    <TextField
                        label="Email"
                        variant="outlined"
                        fullWidth
                        required
                        value={state.username}
                        onChange={(event) => setState({ ...state, username: event.target.value })}
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        label="Password"
                        variant="outlined"
                        type="password"
                        fullWidth
                        required
                        value={state.password}
                        onChange={(event) => setState({ ...state, password: event.target.value })}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Button variant="contained" color="primary" fullWidth type="submit">
                        Sign In
                    </Button>
                </Grid>
                <Grid item xs={12}>
                    <Grid container>
                        <Grid item xs={6}>
                            <Typography align="center" variant="subtitle2">
                                <Link
                                    onClick={() => { setState({ ...state, mode: 'reset-password', errorAlert: { visible: false, type: 'error', text: '' } }) }} // Add your own click handler here
                                    style={{ cursor: "pointer" }}
                                    underline='hover'
                                >
                                    Forgot password?{" "}
                                </Link>

                            </Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography align="center" variant="subtitle2">
                                <Link
                                    onClick={() => { setState({ ...state, password: '', mode: 'create-account', errorAlert: { visible: false, type: 'error', text: '' } }) }} // Add your own click handler here
                                    style={{ cursor: "pointer" }}
                                    underline='hover'
                                >
                                    Sign up
                                </Link>
                            </Typography>
                        </Grid>
                    </Grid>
                </Grid>
            </Fragment>
    }

    return (
        <Container maxWidth="xs">
            <Paper elevation={24} style={{ padding: '24px' }}>
                <form onSubmit={handleSubmit}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}><Typography align="center" variant="h4">Gnome Baseball</Typography></Grid>
                        {annotation}
                        {state.errorAlert.visible ? errorAlertElement : null}
                    </Grid>
                </form>
            </Paper>
        </Container>
    )
};

export default Login;