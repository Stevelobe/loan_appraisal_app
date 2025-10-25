import React, { useState, useEffect } from 'react';
// Assuming the following functions/libraries are available or implemented:
// 1. intcomma: Function to format numbers with commas (e.g., 1000000 -> 1,000,000)
// 2. formatCurrency: Function to format the loan amount (e.g., intcomma(amount) + ' XAF')
// 3. formatDate: Function to format the submission date (e.g., date:"M d, Y H:i")

// Placeholder utilities (replace with actual implementations or imports)
const intcomma = (num) => num.toLocaleString('en-US');
const formatCurrency = (amount) => `${intcomma(parseFloat(amount).toFixed(2))} XAF`;
const formatDate = (dateString) => {
    const options = { month: 'short', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleString('en-US', options);
};

// --- Loan Data Structure (Mock Data) ---
const mockApprovedLoans = [
    {
        pk: 1,
        applicant_name: "Alice Johnson",
        loan_type: "H", // Loan type internal key
        loan_type_display: "Housing Loan", // Result of loan.get_loan_type_display
        loan_amount: 5000000.00,
        annual_interest_rate_percent: 8.5,
        loan_term_years: 15,
        submission_date: "2024-01-10T10:30:00Z",
    },
    {
        pk: 2,
        applicant_name: "Bob Williams",
        loan_type: "C",
        loan_type_display: "Car Loan",
        loan_amount: 1250000.50,
        annual_interest_rate_percent: 7.25,
        loan_term_years: 5,
        submission_date: "2024-02-15T15:45:00Z",
    },
    // Add more mock loans as needed...
];

/**
 * Renders the Approved Loans Overview table, including selection, deletion, and modal logic.
 *
 * @param {object} props
 * @param {Array<object>} props.approvedLoans The list of approved loan objects.
 * @param {Array<object>} props.messages List of Django-style messages for display.
 * @param {function} props.onDeleteSelected Callback function when deletion is confirmed.
 */
const ApprovedLoansOverview = ({
    approvedLoans = mockApprovedLoans, // Use mock data as default
    messages = [], // Example: [{tags: 'success', text: 'Loans deleted successfully'}]
    onDeleteSelected = (pks) => console.log('Deleting loans with pks:', pks),
}) => {
    const [selectedLoans, setSelectedLoans] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState({ title: '', message: '', isError: false });

    const hasLoans = approvedLoans && approvedLoans.length > 0;
    const selectedCount = selectedLoans.length;

    // --- Select All Logic ---
    const handleSelectAll = (e) => {
        if (e.target.checked) {
            const allPks = approvedLoans.map(loan => loan.pk);
            setSelectedLoans(allPks);
        } else {
            setSelectedLoans([]);
        }
    };

    // --- Individual Checkbox Logic ---
    const handleSelectLoan = (pk) => {
        setSelectedLoans(prev => {
            if (prev.includes(pk)) {
                return prev.filter(id => id !== pk);
            } else {
                return [...prev, pk];
            }
        });
    };

    // --- Modal Control Functions ---
    const showModal = (title, message, isError = false) => {
        setModalContent({ title, message, isError });
        setIsModalOpen(true);
    };

    const hideModal = () => {
        setIsModalOpen(false);
    };

    // --- Form Submission / Delete Button Logic ---
    const handleDeleteClick = (e) => {
        e.preventDefault(); // Stop the form from submitting immediately

        if (selectedCount === 0) {
            showModal(
                'No Loans Selected',
                'Please select at least one loan to delete.',
                true
            );
        } else {
            showModal(
                'Confirm Deletion',
                `Are you sure you want to delete ${selectedCount} selected loan(s)? This action cannot be undone.`,
                false
            );
        }
    };

    const handleConfirmDelete = () => {
        hideModal();
        // Call the parent component's delete handler
        onDeleteSelected(selectedLoans);
        // Reset local state after "submission"
        setSelectedLoans([]); 
    };

    // Helper to get Tailwind classes for messages
    const getMessageClasses = (tags) => {
        if (tags === 'success') return 'bg-green-100 text-green-800';
        if (tags === 'error') return 'bg-red-100 text-red-800';
        if (tags === 'warning') return 'bg-yellow-100 text-yellow-800';
        return 'bg-blue-100 text-blue-800';
    };

    return (
        <div className="container mx-auto px-4 py-12 max-w-7xl">
            {/* Page Title */}
            <h1 className="text-5xl font-extrabold text-slate-900 mb-10 text-center border-b-4 border-indigo-500 pb-5">
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-700">Approved Loans Overview</span>
            </h1>

            {/* Messages Display */}
            {messages.length > 0 && (
                <div className="mb-6 space-y-3">
                    {messages.map((message, index) => (
                        <div key={index} className={`p-4 rounded-lg text-sm ${getMessageClasses(message.tags)}`}>
                            {message.text}
                        </div>
                    ))}
                </div>
            )}

            {/* Loans Table or No Loans Message */}
            {hasLoans ? (
                <div className="bg-white rounded-3xl shadow-3xl border border-slate-100 p-8 overflow-x-auto transition-all duration-300 ease-in-out hover:shadow-4xl">
                    {/* Form for Deletion - action URL is hardcoded or passed via props in React */}
                    <form onSubmit={handleDeleteClick}>
                        {/* No need for {% csrf_token %} in React API submission */}
                        <table className="min-w-full divide-y divide-slate-200">
                            <thead className="bg-slate-50">
                                <tr>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider rounded-tl-xl">
                                        <input
                                            type="checkbox"
                                            id="select-all"
                                            className="form-checkbox h-4 w-4 text-indigo-600 transition duration-150 ease-in-out rounded"
                                            checked={selectedCount === approvedLoans.length && selectedCount > 0}
                                            onChange={handleSelectAll}
                                        />
                                    </th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Applicant Name</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Loan Type</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Loan Amount</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Interest Rate</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Loan Term (Years)</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Submission Date</th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider rounded-tr-xl">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-slate-200">
                                {approvedLoans.map((loan) => (
                                    <tr key={loan.pk} className="hover:bg-slate-50 transition-colors duration-150 ease-in-out">
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <input
                                                type="checkbox"
                                                name="selected_loans"
                                                value={loan.pk}
                                                className="form-checkbox h-4 w-4 text-indigo-600 transition duration-150 ease-in-out rounded"
                                                checked={selectedLoans.includes(loan.pk)}
                                                onChange={() => handleSelectLoan(loan.pk)}
                                            />
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{loan.applicant_name}</td>
                                        {/* Use the display value from the data */}
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.loan_type_display}</td>
                                        {/* Use local formatting utilities */}
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{formatCurrency(loan.loan_amount)}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.annual_interest_rate_percent}%</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.loan_term_years}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{formatDate(loan.submission_date)}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                            {/* Replace Django URL with a hardcoded or prop-provided route */}
                                            <a href={`/download-appraisal-pdf/${loan.pk}`} className="text-indigo-600 hover:text-indigo-900 mr-4 transition-colors duration-150 ease-in-out">Download PDF</a>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        
                        {/* Delete Button */}
                        <div className="mt-6 flex justify-end">
                            <button 
                                type="submit" 
                                id="delete-button" 
                                className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-full shadow-sm text-white transition duration-150 ease-in-out 
                                    ${selectedCount > 0 ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' : 'bg-red-400 cursor-not-allowed'}`
                                }
                                disabled={selectedCount === 0}
                            >
                                <svg className="-ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1zm2 3a1 1 0 011-1h4a1 1 0 110 2H9a1 1 0 01-1-1z" clipRule="evenodd" />
                                </svg>
                                Delete Selected Loans
                            </button>
                        </div>
                    </form>
                </div>
            ) : (
                <p className="text-center text-gray-600 text-lg">No approved loan applications found.</p>
            )}

            {/* Custom Confirmation Modal */}
            <div 
                id="confirmation-modal" 
                className={`fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center z-50 ${isModalOpen ? '' : 'hidden'}`}
                onClick={hideModal} // Close on backdrop click
            >
                <div 
                    className="bg-white rounded-lg shadow-xl p-8 max-w-sm w-full mx-4"
                    onClick={e => e.stopPropagation()} // Prevent modal closing when clicking inside
                >
                    <div className="text-center">
                        <svg className="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                        </svg>
                        <h3 
                            className={`mt-4 text-lg leading-6 font-medium ${modalContent.isError ? 'text-red-600' : 'text-gray-900'}`} 
                            id="modal-title"
                        >
                            {modalContent.title}
                        </h3>
                        <div className="mt-2">
                            <p className="text-sm text-gray-500" id="modal-message">
                                {modalContent.message}
                            </p>
                        </div>
                    </div>
                    <div className="mt-5 sm:mt-6 sm:flex sm:flex-row-reverse">
                        {!modalContent.isError && (
                            <button 
                                type="button" 
                                id="confirm-delete-button" 
                                onClick={handleConfirmDelete}
                                className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm transition duration-150 ease-in-out"
                            >
                                Delete
                            </button>
                        )}
                        <button 
                            type="button" 
                            id="cancel-delete-button" 
                            onClick={hideModal}
                            className={`mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:w-auto sm:text-sm transition duration-150 ease-in-out ${modalContent.isError ? 'w-full' : ''}`}
                        >
                            {modalContent.isError ? 'Close' : 'Cancel'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ApprovedLoansOverview;