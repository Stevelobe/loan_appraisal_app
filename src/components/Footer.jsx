import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative z-20 bg-gradient-to-r from-indigo-900/80 to-purple-900/80 text-white py-8 mt-12 shadow-inner">
      <div className="container mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="col-span-1">
          <h3 className="text-xl font-bold mb-4 text-indigo-200">
            Mubaku Loan Appraisal
          </h3>
          <p className="text-indigo-100 text-sm">
            Empowering Banks and MFIs with streamline loan appraisal and compliance
            tool.
          </p>
        </div>
        <div className="col-span-1">
          <h3 className="text-xl font-bold mb-4 text-indigo-200">Quick Links</h3>
          <ul className="space-y-2">
            <li>
              <a
                href="/loan-selection"
                className="text-indigo-100 hover:text-white transition-colors duration-200 text-sm"
              >
                Home
              </a>
            </li>
            {/* If user context is passed, you can conditionally render here */}
            <li>
              <a
                href="/approved-loans-list"
                className="text-indigo-100 hover:text-white transition-colors duration-200 text-sm"
              >
                Approved Loans
              </a>
            </li>
            <li>
              <a
                href="/loan-review-dashboard"
                className="text-indigo-100 hover:text-white transition-colors duration-200 text-sm"
              >
                Loans Under Review
              </a>
            </li>
          </ul>
        </div>
        <div className="col-span-1">
          <h3 className="text-xl font-bold mb-4 text-indigo-200">Contact Support</h3>
          <ul className="space-y-2 text-sm">
            <li>
              <a
                href="mailto:Mubakuhightech2022@gmail.com"
                className="text-indigo-100 hover:text-white transition-colors duration-200 flex items-center"
              >
                <svg
                  className="w-4 h-4 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                Mubakuhightech2022@gmail.com
              </a>
            </li>
            <li>
              <a
                href="tel:+237671487555"
                className="text-indigo-100 hover:text-white transition-colors duration-200 flex items-center"
              >
                <svg
                  className="w-4 h-4 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.774a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                </svg>
                +237 671487555
              </a>
            </li>
            <li className="text-indigo-100 flex items-center">
              <svg
                className="w-4 h-4 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l3 3a1 1 0 001.414-1.414L11 9.586V6z"
                  clipRule="evenodd"
                />
              </svg>
              Response time: Within 24 hours
            </li>
          </ul>
        </div>
      </div>
      <div className="text-center text-sm text-indigo-300 mt-8 pt-6 border-t border-indigo-700">
        &copy; {currentYear} Mubaku High-Tech Incorporation. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;
