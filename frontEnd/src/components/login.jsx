import React, { useState } from 'react';
import LoginUI from '../view/login';

const Login = () => {

    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [isLogged, setIsLogged] = useState(false);
    const [authFail, setAuthFail] = useState(false);
    
    const checkAccount = () => {
        if (user === "Aitana" && password === "410") {
            let userString = JSON.stringify(user);
            let passwordString = JSON.stringify(password);
            localStorage.setItem('user', userString);
            localStorage.setItem('password', passwordString);
            setAuthFail(false);
            setIsLogged(true);
        } else {
            setPassword('');
            setAuthFail(true);
            setIsLogged(false);
        }  
    };

    return (    
        <LoginUI
            user={user} 
            password={password} 
            isLogged={isLogged}
            authFail={authFail} 
            setUser={(newUser) => {setUser(newUser)}} 
            setPassword={(newPassword) => {setPassword(newPassword)}} 
            checkAccount={checkAccount}
        />
    );
}

export default Login;
