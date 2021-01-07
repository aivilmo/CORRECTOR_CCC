import React from 'react';
import { Box, Button, Typography } from '@material-ui/core';
import { Redirect } from 'react-router-dom';

class HomeUI extends React.Component {

    render() {
        return (
            <div className="center">
                <Box mt={5}> 
                    <Typography variant="h4" color="initial" > 
                    Bienvenido, {this.props.user} !
                    </Typography>
                </Box>
                <Box mt={25}>
                    <Button color="primary" variant="contained" onClick={this.props.openDocs}>
                        Correct open docs
                    </Button>
                </Box>
                <Box mt={5}>
                    <Button color="primary" variant="contained" onClick={this.props.pendingDocs}>
                        Correct pending docs
                    </Button>
                </Box>
                <Box mt={5}>
                    <Button color="secondary" variant="contained" onClick={this.props.logout}>
                        Logout
                    </Button>
                </Box>
                {!this.props.isLogged && <Redirect to="/" > </Redirect>}
            </div>
        );
    }   
}

export default HomeUI;