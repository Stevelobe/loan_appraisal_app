import React from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

// 1. Define the Validation Schema using Yup
const validationSchema = yup.object().shape({
  username: yup.string().required('Username is required.'),
  password: yup.string().required('Password is required.').min(6, 'Password must be at least 6 characters.'),
});

// 2. Define the Form Fields (Used for mapping and display)
const formFields = [
  { name: 'username', label: 'Username', type: 'text', helpText: 'Enter your system username.' },
  { name: 'password', label: 'Password', type: 'password', helpText: 'Must be 6+ characters.' },
];

/**
 * Renders a Login form styled with Tailwind CSS, using React Hook Form and Yup validation.
 */
const LoginForm = () => {
  // Setup React Hook Form with Yup resolver
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting, nonFieldErrors } 
  } = useForm({
    resolver: yupResolver(validationSchema),
    // You can set default values here if needed
    defaultValues: {
        username: '',
        password: '',
    },
  });

  // Function to handle form submission
  const onSubmit = (data) => {
    // This is where you would send the data to your API (e.g., using fetch or Axios)
    console.log('Form Submitted:', data);
    
    return new Promise((resolve) => {
      // Simulate an API call delay
      setTimeout(() => {
        // In a real app, check the API response for errors
        // If there were API errors, you'd use setError('username', ...) or setErrors(nonFieldErrors: [...])
        alert(`Login successful for ${data.username}! (Simulated)`);
        resolve();
      }, 1000);
    });
  };

  // Function to apply required base styles to inputs
  const getInputClasses = (fieldName) => `
    w-full p-3 border rounded-lg focus:outline-none transition duration-150 ease-in-out 
    ${errors[fieldName] ? 'border-red-500 focus:ring-red-500' : 'border-slate-300 focus:border-indigo-500 focus:ring-indigo-500'}
  `;

  return (
    <div className="flex justify-center mt-5">
      <div className="w-full max-w-md">
        <div className="bg-white shadow-xl rounded-xl mt-5 overflow-hidden mx-4 sm:mx-0">
          
          {/* Header Section */}
          <div className="bg-indigo-700 text-white text-center py-4 rounded-t-xl">
            <h3 className="font-semibold text-2xl my-4">Login</h3>
          </div>
          
          {/* Form Body */}
          <div className="p-6 text-slate-800">
            <form onSubmit={handleSubmit(onSubmit)} noValidate>
              
              {/* Map over the defined fields */}
              {formFields.map((field) => (
                // Replicating the 'field-wrapper' concept
                <div key={field.name} className="mb-4">
                  
                  {/* Label Tag */}
                  <label 
                    htmlFor={field.name} 
                    className="block mb-2 font-semibold text-slate-700"
                  >
                    {field.label}
                  </label>
                  
                  {/* Input Field - uses React Hook Form's register */}
                  <input
                    id={field.name}
                    type={field.type}
                    placeholder={`Enter ${field.label.toLowerCase()}`}
                    className={getInputClasses(field.name)}
                    {...register(field.name)}
                  />
                  
                  {/* Help Text */}
                  {field.helpText && !errors[field.name] && (
                    <div className="text-sm text-slate-500 mt-1">{field.helpText}</div>
                  )}
                  
                  {/* Field Errors */}
                  {errors[field.name] && (
                    <div className="text-red-600 text-sm mt-1">{errors[field.name].message}</div>
                  )}
                </div>
              ))}
              
              {/* Non-Field Errors (for general API errors like "Invalid Credentials") */}
              {/* RHF nonFieldErrors is often an array; here we check a custom state or errors.root */}
              {errors.root?.message && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md relative mb-4">
                    <p>{errors.root.message}</p>
                </div>
              )}
              
              {/* Submit Button */}
              <div>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl transition-colors duration-200 mt-3 disabled:opacity-50"
                >
                  {isSubmitting ? 'Logging in...' : 'Log In'}
                </button>
              </div>
            </form>
          </div>
          
          {/* Footer Section */}
          <div className="text-center py-4 bg-slate-100 text-slate-600 rounded-b-xl">
            {/* You can add links here, e.g., */}
            <a href="/register" className="hover:text-indigo-600 transition">Need an account? Sign Up</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;