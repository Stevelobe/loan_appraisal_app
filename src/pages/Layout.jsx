import React from 'react';
import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
const Layout = () => {
  return (
    <div className="relative min-h-screen flex flex-col overflow-x-hidden "
        style={{backgroundImage: "url('/assets/background.jpeg')",
            backgroundSize: "cover", 
            backgroundPosition: "center"
         }}
    >
      <div className="fixed top-0 left-0 w-full h-full -z-10 bg-black/10"></div>
      <div className="z-20">
        <Navbar />
      </div>
      <main className="flex-grow relative z-10">
        <Outlet />
      </main>
      <div className="z-20">
        <Footer />
      </div>
    </div>
  );
};

const RequireAuth = () =>{
    return(
        <div>

        </div>
    )
}

export {Layout, RequireAuth}