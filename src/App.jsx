import React from "react";
import {
  createBrowserRouter, 
  RouterProvider,
} from "react-router-dom";
import Login from "./pages/Login";
import LoanSelection from "./pages/LoanApplicationDashboad";
import {Layout,  RequireAuth } from "../src/pages/Layout";
import CobacRegulations from "./pages/Reculation";
import HomePage from "./pages/HomePage";
const App = () =>{
  const router = createBrowserRouter([
    {
      path: '/',
      element: <Layout/>,
      children:[
        {
          path: "/",
          element: <HomePage/>
        },
        {
          path: "/dashboard",
          element: <LoanSelection/>
        },
        {
          path: "/login",
          element: <Login/>
        },
        {
          path: "/regulations",
          element: <CobacRegulations/>
        }
      ]
    },
    // {
    //   path: "/",
    //   element: <RequireAuth/>,
    //   children: [
    //     {
    //       path: "/profile",
    //       element: <ProfilePage/>,
    //       loader: profilePageLoader
    //     },
    //     {
    //       path: "/profile/update",
    //       element: <ProfileUpdatePage/>
    //     },
    //     {
    //       path: "/profile/newpost",
    //       element: <NewPostPage/>
    //     }
    //   ]
    // }
  ])
  return (
    <RouterProvider router={router}/>
  );
}

export default App;