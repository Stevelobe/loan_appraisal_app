import React from "react";
import {
  createBrowserRouter, 
  RouterProvider,
} from "react-router-dom";
import Login from "./pages/Login";
import LoanSelection from "./pages/LoanApplicationDashboad";
import {Layout,  RequireAuth } from "../src/pages/Layout";
import ApprovedLoansOverview from "./pages/ApprovedLoans";
import LoanReviewDashboard from "./pages/LoanUnderReview";
import CobacRegulations from "./pages/Reculation";
import HomePage from "./pages/HomePage";
import { allLoans } from "./lib/loaders";
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
        },
        {
          path: "/approved-loans",
          element: <ApprovedLoansOverview/>,
          loader: allLoans,
        },
        {
          path: "/loan-review",
          element: <LoanReviewDashboard/>
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