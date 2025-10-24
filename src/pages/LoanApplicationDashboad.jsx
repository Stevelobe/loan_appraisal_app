import React, { useState } from 'react';

const LoanSelection = ({
  totalApprovedLoans = 0, // Default to 0 for a cleaner demo
  loanTypes = [ // Example structure for loanTypes
    { value: 'mortgage-loan', label: 'Mortgage Loan' },
    { value: 'salary-loan', label: 'Salary-Backed Loan' },
    { value: 'loan-within-saving', label: 'Loan Within Savings' },
    { value: 'daily-loan', label: 'Daily Savings Loan' },
    { value: 'stading-loan', label: 'Standing Order Loan' },
    { value: 'real-estate-loan', label: 'Real Estate Loan' },
    { value: 'container-loan', label: 'Container Loan' },
    { value: 'agricultural-loan', label: 'Agricultural Loan' },
    { value: 'express-loan', label: 'Express Loan' },
    { value: 'business-loan', label: 'Business Loan' },
  ],
  recentApplications = [], // Example structure for recentApplications, pass empty array if none
  onLoanSelect, // Function to handle form submission
  getLoanTypeDisplay = (type) => type.toUpperCase(), // Helper for display text
}) => {
  const [selectedLoanType, setSelectedLoanType] = useState(loanTypes.length > 0 ? loanTypes[0].value : '');
  const [error, setError] = useState(null); // State for form error

  // Simple animation utility class, often added via a library like `animate.css` or defined in index.css
  const animatePulseSlight = 'animate-pulse-slight';

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedLoanType) {
      setError(null);
      // In a real React app, this would typically call an API or a router function.
      onLoanSelect(selectedLoanType);
    } else {
      setError('Please select a loan type before proceeding.');
    }
  };

  // Helper function to render application status text and color
  const getStatusText = (approved) => {
    if (approved === true) return { text: 'Approved', color: 'text-green-700' };
    if (approved === false) return { text: 'Declined', color: 'text-red-700' };
    return { text: 'Review', color: 'text-yellow-700' };
  };

  return (
    // Equivalent to 'calculator/base.html' content area
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Main flex container to arrange content side-by-side */}
      <div className="flex flex-col md:flex-row justify-center items-start gap-6 lg:gap-8">

        {/* --- Left Column: Loan Selection and Approved Loans Count --- */}
        <div className="w-full md:w-1/2 lg:w-2/5 p-4 sm:p-5 bg-white rounded-xl shadow-lg space-y-5 border border-slate-200 text-slate-900 transform transition-all duration-300 ease-in-out hover:scale-[1.005]">

          {/* Page Title Section */}
          <div className="text-center pb-2 border-b-2 border-indigo-400">
            <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 leading-tight">
              Select Loan Product
            </h2>
            <p className="mt-1 text-sm text-slate-600">
              Choose the type of loan to appraise.
            </p>
          </div>

          {/* Total Loans Granted Section */}
          <div className={`text-center p-3 bg-blue-500/10 border border-blue-500 rounded-lg shadow-sm ${animatePulseSlight}`}>
            <p className="text-base sm:text-lg font-semibold mb-1 text-blue-900">
              Total Loans Granted:
            </p>
            <p className="text-3xl sm:text-4xl font-extrabold text-blue-700 leading-tight">
              {totalApprovedLoans.toLocaleString('en-US')}
            </p>
            <p className="text-xs text-blue-800 mt-0.5">
              Count updates as new loans are approved.
            </p>
          </div>

          {/* Navigation Buttons Section */}
          <div className="text-center pt-2 pb-4 border-b border-slate-200">
            <h3 className="text-base font-semibold text-slate-700 mb-2">Quick Actions</h3>
            <div className="flex flex-col sm:flex-row justify-center items-center gap-2">
              <a href="/approved-loans" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-all duration-300 ease-in-out transform hover:-translate-y-0.5">
                <svg className="-ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2zm0 6a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2z" clipRule="evenodd" />
                </svg>
                View Approved Loans
              </a>
              <a href="/regulations" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 ease-in-out transform hover:-translate-y-0.5">
                <svg className="-ml-1 mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0113 3.414L16.586 7A2 2 0 0117 8.414V16a2 2 0 01-2 2H5a2 2 0 01-2-2V4zm5 2a1 1 0 00-1 1v3a1 1 0 01-2 0V7a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h12a1 1 0 001-1V8a1 1 0 00-1-1h-3a1 1 0 00-1 1v3a1 1 0 01-2 0V8a1 1 0 00-1-1H9z" clipRule="evenodd"></path>
                </svg>
                Regulations
              </a>
            </div>
          </div>

          {/* Loan Type Selection Form Section */}
          <div className="max-w-xs mx-auto pt-3">
            <h3 className="text-base font-semibold text-slate-700 mb-2 text-center">Start a New Appraisal</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* CSRF token is not needed in a stateless React component talking to an API */}
              <div className="field-wrapper">
                <label htmlFor="loan_type_select" className="block text-sm font-semibold text-slate-700 mb-1">
                  Loan Type
                </label>
                <select
                  id="loan_type_select"
                  name="loan_type"
                  value={selectedLoanType}
                  onChange={(e) => setSelectedLoanType(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md shadow-sm"
                  required
                >
                  {/* Map the loan types from props to options */}
                  {loanTypes.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
                {/* Error message display */}
                {error && (
                  <p className="mt-1 text-xs text-red-600 font-medium flex items-center">
                    <span className="mr-1 text-base">⚠️</span> {error}
                  </p>
                )}
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-700 hover:from-indigo-700 hover:to-purple-800 text-white font-bold py-2.5 px-4 rounded-md shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-indigo-400 transition-all duration-300 ease-in-out transform hover:-translate-y-0.5 mt-3 flex items-center justify-center text-base tracking-wide"
              >
                <span className="mr-2 text-lg">➡️</span> Proceed
              </button>
            </form>
          </div>

        </div>

        {/* --- Right Column: Recent Activity/Statistics --- */}
        <div className="w-full md:w-1/2 lg:w-3/5 p-4 sm:p-5 bg-white rounded-xl shadow-lg space-y-5 border border-slate-200 text-slate-900 transform transition-all duration-300 ease-in-out hover:scale-[1.005] md:ml-auto">
          <div className="text-center pb-2 border-b-2 border-green-400">
            <h3 className="text-xl sm:text-2xl font-extrabold text-slate-900 leading-tight">
              Recent Application Activity
            </h3>
            <p className="mt-1 text-sm text-slate-600">
              Latest loan applications submitted.
            </p>
          </div>

          {/* Conditional rendering for recent applications */}
          {recentApplications && recentApplications.length > 0 ? (
            <>
              <ul className="space-y-3">
                {recentApplications.map((app, index) => {
                  const status = getStatusText(app.approved);
                  return (
                    // Assuming 'id' is a unique key for list items in a real app
                    <li key={index} className="p-3 bg-green-50/50 rounded-lg border border-green-200 flex items-center justify-between shadow-sm">
                      <div>
                        <p className="font-semibold text-slate-800 text-base">{app.applicant_name}</p>
                        {/* Assuming loan_amount is a number and app.loan_type is a string/value */}
                        <p className="text-sm text-slate-600">
                          {getLoanTypeDisplay(app.loan_type)} - {app.loan_amount.toLocaleString('en-US')} XAF
                        </p>
                      </div>
                      <span className={`text-xs font-medium ml-2 ${status.color}`}>
                        {status.text}
                      </span>
                    </li>
                  );
                })}
              </ul>
              <div className="text-center mt-4">
                <a href="/approved-loans" className="text-sm text-indigo-600 hover:text-indigo-800 font-medium transition-colors duration-200">
                  View All Applications →
                </a>
              </div>
            </>
          ) : (
            <div className="text-center p-6 bg-blue-50/50 rounded-lg border border-blue-200 text-blue-800">
              <p className="text-base font-medium">No recent applications found.</p>
              <p className="text-sm mt-1">Submit a new loan application to see activity here.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default LoanSelection;

// NOTE: You would typically define a slight pulse animation in your global CSS (e.g., index.css or a dedicated stylesheet).
// For example:
// @keyframes pulse-slight {
//   0%, 100% { transform: scale(1); }
//   50% { transform: scale(1.005); }
// }
// .animate-pulse-slight {
//   animation: pulse-slight 3s infinite ease-in-out;
// }