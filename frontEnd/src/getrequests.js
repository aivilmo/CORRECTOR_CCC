import { useState, useEffect } from 'react';

function GetRequests() {
    
    useEffect(()=> {
        fetch('/fun').then(response => response.json()).then(data => console.log(data))
    });
}

export default GetRequests;