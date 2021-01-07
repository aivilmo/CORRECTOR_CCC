import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Login from './components/login.jsx';
import Home from './components/home.jsx';


function App() {  

    return (
        <Router> 
            <div className="App">
                <Switch> 
                    <Route path="/home">
                        <Home> </Home>
                    </Route>
                    <Route path="/">
                        <Login/>
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}

export default App;
