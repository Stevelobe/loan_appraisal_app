import React, { useState, useCallback } from 'react';
import { Navigate, Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar';
const Layout = () =>{
    return(          
        <div className='layout'>
       <div className='navbar'>
      
       </div>
       <div className='content'>
        <Outlet/>
       </div>
     </div>
       
    )
}

const RequireAuth = () =>{
    return(
        <div>

        </div>
    )
}

export {Layout, RequireAuth}