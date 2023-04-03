import React from "react";

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.user = '';
        this.password = '';
    }

    async componentDidMount(){

    }

    componentWillUnmount() {

    }

    onKeyDown(key) {
        if(e.key == 'Enter')
            this.props.attemptLogin({user:this.user, password:this.password});
    }

    createAccount() {

    }


    render () {
        return (
            <div>
                
            </div>
        )
    }
}