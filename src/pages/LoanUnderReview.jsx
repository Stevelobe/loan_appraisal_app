import React from 'react';

// Placeholder utility functions to mimic Django filters
// Replace these with actual library imports (e.g., `date-fns`, `numeral`, or custom utils)
const intcomma = (num) => num.toLocaleString('en-US');
const formatCurrency = (amount) => `${intcomma(parseFloat(amount).toFixed(2))} XAF`;
const formatDate = (dateString) => {
    // Mimics date:"M d, Y H:i"
    const options = { month: 'short', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleString('en-US', options);
};

// Mock data to simulate the Django context variable 'loans_under_review'
const mockLoans = [
    {
        pk: 101,
        applicant_name: "Emma Stone",
        loan_type: "P", // Personal Loan
        get_loan_type_display: "Personal Loan",
        loan_amount: 850000.00,
        submission_date: "2024-10-20T09:15:00Z",
    },
    {
        pk: 102,
        applicant_name: "David Chen",
        loan_type: "B", // Business Loan
        get_loan_type_display: "Small Business Loan",
        loan_amount: 12000000.00,
        submission_date: "2024-10-21T14:40:00Z",
    },
    {
        pk: 103,
        applicant_name: "Sarah Lee",
        loan_type: "E", // Education Loan
        get_loan_type_display: "Education Loan",
        loan_amount: 450000.00,
        submission_date: "2024-10-23T11:05:00Z",
    },
];

/**
 * Renders the Loan Review Dashboard showing loans currently under review.
 *
 * @param {object} props
 * @param {Array<object>} props.loansUnderReview The list of loan applications currently being reviewed.
 * @param {string} props.backUrl The URL for the "Back to Loan Selection" link.
 */
const LoanReviewDashboard = ({
    loansUnderReview = mockLoans, // Use mock data as default
    backUrl = '/loan-selection', // Corresponds to Django's {% url 'loan_selection' %}
}) => {
    const hasLoans = loansUnderReview && loansUnderReview.length > 0;

    return (
        <div className="container mx-auto px-4 py-12 max-w-7xl">
            {/* Page Title */}
            <h1 className="text-4xl font-extrabold text-slate-900 mb-8 text-center border-b-4 border-indigo-500 pb-4">
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-700">Loan Review Dashboard</span>
            </h1>

            <div className="bg-white rounded-3xl shadow-3xl border border-slate-100 p-8 mb-8">
                <h2 className="text-2xl font-bold text-slate-800 mb-6 border-b pb-3">Loans Under Review</h2>

                {/* Conditional rendering based on loans_under_review data */}
                {hasLoans ? (
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-slate-200 rounded-lg overflow-hidden">
                            <thead className="bg-indigo-500">
                                <tr>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider rounded-tl-lg">Applicant Name</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Loan Type</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Loan Amount</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider rounded-tr-lg">Submission Date</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-slate-200">
                                {/* Looping over the loans_under_review data */}
                                {loansUnderReview.map((loan, index) => (
                                    <tr key={loan.pk} className={`hover:bg-purple-50 transition-colors duration-200 ease-in-out ${index % 2 === 1 ? 'bg-slate-50' : ''}`}>
                                        <td className="px-6 py-4 whitespace-nowrap text-base font-medium text-slate-900">{loan.applicant_name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{loan.get_loan_type_display}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{formatCurrency(loan.loan_amount)}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{formatDate(loan.submission_date)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p className="text-slate-600 text-center py-8">No loan applications currently under review.</p>
                )}
            </div>

            {/* Back Button */}
            <div className="flex justify-center mt-8">
                <a 
                    href='/dashboard'
                    className="inline-flex items-center px-6 py-3 border border-slate-300 text-base font-medium rounded-full shadow-sm text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 ease-in-out"
                >
                    <svg className="-ml-1 mr-3 h-5 w-5 text-slate-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    Back to Loan Selection
                </a>
            </div>
        </div>
    );
};

export default LoanReviewDashboard;