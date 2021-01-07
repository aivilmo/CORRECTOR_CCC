import React, { useState } from 'react';
import HomeUI from '../view/home';
import GetRequests from '../getrequests';

const Home = () => {

    const [user] = useState(localStorage.getItem('user'));
    const [isLogged, setIsLogged] = useState(true);

    const openDocs = () => {
        GetRequests();
    };

    const pendingDocs = () => {

    };

    const logout = () => {
        setIsLogged(false);
        localStorage.removeItem('user');
        localStorage.removeItem('password');
    };

    return (    
        <HomeUI 
            user={user}
            isLogged={isLogged}
            openDocs={openDocs}
            pendingDocs={pendingDocs}
            logout={logout}
        />
    );
}

export default Home;

