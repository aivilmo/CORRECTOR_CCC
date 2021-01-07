import React from 'react';
import { Box, Button, TextField } from '@material-ui/core';
import { Redirect } from 'react-router-dom';

class LoginUI extends React.Component {

    render() {
        return (
            <div className="center">
                <Box mt={25}>
                    <form mr="2000">
                        <Box mx={1}>
                            <TextField label="User" color="secondary" onChange={(e) => this.props.setUser(e.target.value)}/>
                        </Box>
                        {!this.props.authFail && <TextField label="Password" color="secondary" type="password" 
                            onChange={(e) => this.props.setPassword(e.target.value)}/>}
                        {this.props.authFail && <TextField error label="Password" color="secondary" type="password" helperText="Incorrect user or password" 
                            value={this.props.password} onChange={(e) => this.props.setPassword(e.target.value)}/>}
                    </form>
                </Box>
                <Box my={5}>
                    <Button color="secondary" variant="contained" onClick={this.props.checkAccount}>
                        Login
                    </Button>
                    {this.props.isLogged && <Redirect to="/home"> </Redirect>}
                </Box>
            </div>
        );
    }   
}

export default LoginUI;


