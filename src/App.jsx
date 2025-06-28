import React from "react";
import {
  createBrowserRouter, 
  RouterProvider,
} from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import LoanApplicationPage from "./pages/LoanApplicationPage";
import {Layout,  RequireAuth } from "../src/pages/Layout";
const App = () =>{
  const router = createBrowserRouter([
    {
      path: '/',
      element: <Layout/>,
      children:[
        // {
        //   path: "/",
        //   element: <HomePage/>
        // },
        // {
        //   path: "/list",
        //   element: <ListPage/>,
        //   loader: listPageLoader
        // },
        // {
        //   path: "/:id",
        //   element: <SinglePage/>,
        //   loader: singlePageLoader
        // },
        {
          path: "/dashboard",
          element: <Dashboard/>
        },
        {
          path: "/login",
          element: <Login/>
        },
        {
          path: "/apply/:loanType",
          element: <LoanApplicationPage/>
        },
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