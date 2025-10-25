import React from "react";
import logo from '/assets/M.PNG'
const Navbar =()=>{
    return (
    <header className="relative z-20 bg-gradient-to-r from-indigo-900/90 to-purple-900/80 shadow-xl py-4 sm:py-6">
      <div className="container mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-3">
          <img
            src={logo}
            alt="Mubaku Logo"
            className="h-10 w-auto rounded-lg shadow-md"
          />
          <a
            href="/loan-selection"
            className="text-white text-2xl font-bold tracking-tight hover:text-indigo-200 transition-colors duration-200"
          >
            Mubaku Loan Appraisal
          </a>
        </div>
        <nav>
          <ul className="flex flex-wrap justify-center sm:justify-end space-x-4 sm:space-x-6 text-lg">
            <li>
              <a
                href="/"
                className="text-white hover:text-indigo-200 transition-colors duration-200 font-medium px-2 py-1 rounded-md"
              >
                Home
              </a>
            </li>

            <li>
              <a
                href="/dashboard"
                className="text-white hover:text-indigo-200 transition-colors duration-200 font-medium px-2 py-1 rounded-md"
              >
                Dashboard
              </a>
            </li>
            
              <>
                <li>
                  <a
                    href="/approved-loans"
                    className="text-white hover:text-indigo-200 transition-colors duration-200 font-medium px-2 py-1 rounded-md"
                  >
                    Approved Loans
                  </a>
                </li>
                <li>
                  <a
                    href="/loan-review"
                    className="text-white hover:text-indigo-200 transition-colors duration-200 font-medium px-2 py-1 rounded-md"
                  >
                    Loans Under Review
                  </a>
                </li>
                <li className="flex items-center text-indigo-200 font-medium px-2 py-1 rounded-md">
                  Welcome,
                </li>
                <li>
                  <button
                    
                    className="text-white bg-red-600 hover:bg-red-700 transition-colors duration-200 font-medium px-3 py-1 rounded-md"
                  >
                    Logout
                  </button>
                </li>
              </>
            
              <li>
                <a
                  href="/login"
                  className="text-white hover:text-indigo-200 transition-colors duration-200 font-medium px-2 py-1 rounded-md"
                >
                  Login
                </a>
              </li>
         
          </ul>
        </nav>
      </div>
    </header>
  );
}
export default Navbar;