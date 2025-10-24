// src/components/LoginForm.jsx
import React, { useState, useContext } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { FaSignInAlt, FaEye, FaEyeSlash } from 'react-icons/fa';
// import { ToastContainer, toast } from "react-toastify";
// import apiRequest from '../lib/apiRequest';
// import {AuthContext} from '../context/AuthContext'
import { Link, useNavigate } from 'react-router-dom';
// import { ACCESS_TOKEN, REFRESH_TOKEN } from '../lib/constants';

const schema = yup.object().shape({
  name: yup.string().required("Username is required."),
  password: yup.string().required("Password is required."),
});

const LoginForm = ({ onLogin }) => {
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState()
    const [isLoading, setIsLoading] = useState(false)
    const navigate = useNavigate()
    // const {updateUser} = useContext(AuthContext)
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (e) => {
        // setIsLoading(true)
        // const username = e.name
        // const password = e.password
        // try{
        //     const res = await apiRequest.post("/auth/login/", {
        //         username,password
        //     })
        //     localStorage.setItem(ACCESS_TOKEN, res.data.access)
        //     localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
        //     updateUser(res.data)
        //     navigate("/dashboard")
        // }catch(err){
        //     //console.log(err.response?.data)
        //     setError(err.response?.data?.detail)  
        // }finally{
        //     setIsLoading(false)
        // }
  };
  
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="flex items-center justify-center min-h-screen ">
      <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-lg border border-gray-200">
        <div className="flex flex-col items-center">
          
          <FaSignInAlt className="text-blue-500 text-5xl mb-4" />
          <h2 className="text-2xl font-bold text-center text-gray-800">
            Sign in to your account
          </h2>
          <p className="mt-2 text-sm text-center text-gray-600">
           Enter your information below.
          </p>
          <p className="mt-1 text-sm text-red-600">{error}</p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="name">
              User Name
            </label>
            <input
              id="name"
              type="text"
              {...register("name")} 
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Your username"
            />
            {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>}
          </div>
          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              {...register("password")}
              className="w-full pr-10 px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="••••••••"
            />
            <button
              type="button"
              onClick={togglePasswordVisibility}
              className="absolute inset-y-0 right-0 top-6 pr-3 flex items-center text-gray-400 hover:text-gray-600"
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </button>
            {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>}
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Se connecter
          </button>
        </form>
        <div className="text-center py-4 bg-slate-100 text-slate-600 rounded-b-xl">
            {/* You can add links here, e.g., */}
            <a href="/register" className="hover:text-indigo-600 transition">Need an account? Sign Up</a>
          </div>
      </div>
    </div>
  );
};

export default LoginForm;