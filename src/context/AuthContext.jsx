import {  createContext, useEffect, useState } from "react";
import React from "react";
export const AuthContext = createContext()

export const AuthContextProvider = ({children})=>{
    
    const [currentUser, setCurrentUser] = useState(() => {
        const storedUser = localStorage.getItem('user');
        try {
            return storedUser ? JSON.parse(storedUser) : null;
        } catch (error) {
            console.error("Error parsing JSON from localStorage:", error);
            return null; 
        }
    });
    const updateUser=(data)=>{
        setCurrentUser(data)
    }

    useEffect(()=>{
        localStorage.setItem("user", JSON.stringify(currentUser))
    },[currentUser])
    return(
         <AuthContext.Provider value={{currentUser,updateUser}}>
            {children}
        </AuthContext.Provider>
    )
}