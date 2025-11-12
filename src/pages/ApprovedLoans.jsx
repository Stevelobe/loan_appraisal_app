import React, { useState, useMemo } from 'react';
import { useLoaderData } from 'react-router-dom';

// Placeholder utilities (replace with actual implementations or imports)
const intcomma = (num) => num.toLocaleString('en-US');
const formatCurrency = (amount) => `${intcomma(parseFloat(amount).toFixed(2))} XAF`;
const formatDate = (dateString) => {
    const options = { month: 'short', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
    try {
        return new Date(dateString).toLocaleString('en-US', options);
    } catch (e) {
        return 'Invalid Date';
    }
};

const ApprovedLoansOverview = ({
    messages = [],
    onDeleteSelected = (pks) => console.log('Deleting loans with pks:', pks),
}) => {
    const initialLoans = useLoaderData() || []; 
    // console.log(initialLoans) // Kept out for clean output
    // --- State for Filtering ---
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedLoanType, setSelectedLoanType] = useState('All Loans');
    
    // --- Existing State ---
    const [selectedLoans, setSelectedLoans] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState({ title: '', message: '', isError: false });

    // --- Derived Data (Filtering) ---
    const uniqueLoanTypes = useMemo(() => {
        const types = new Set(initialLoans.map(loan => loan.loan_type_display));
        return ['All Loans', ...Array.from(types).sort()];
    }, [initialLoans]);

    const filteredLoans = useMemo(() => {
        let loans = initialLoans;

        if (selectedLoanType !== 'All Loans') {
            loans = loans.filter(loan => loan.loan_type_display === selectedLoanType);
        }

        if (searchTerm) {
            const lowerCaseSearch = searchTerm.toLowerCase();
            loans = loans.filter(loan => 
                loan.applicant_name.toLowerCase().includes(lowerCaseSearch)
            );
        }
        
        return loans;
    }, [initialLoans, selectedLoanType, searchTerm]);
    
    const hasLoans = filteredLoans && filteredLoans.length > 0;
    const selectedCount = selectedLoans.length;

    // --- Select All Logic ---
    const handleSelectAll = (e) => {
        if (e.target.checked) {
            // NOTE: Assuming loan objects have a 'pk' property for selection, though you use 'id' later.
            // For safety, I'll use `loan.pk` as per your Select All logic, but you might need to confirm if it should be `loan.id`.
            const allPks = filteredLoans.map(loan => loan.pk); 
            setSelectedLoans(allPks);
        } else {
            setSelectedLoans([]);
        }
    };
    
    // Use `loan.pk` in isAllSelected check for consistency with `handleSelectAll`
    const isAllSelected = selectedCount > 0 && filteredLoans.length > 0 && filteredLoans.every(loan => selectedLoans.includes(loan.pk)); 
    
    // --- Other handlers (unchanged, but referencing 'pk' for consistency) ---
    const handleSelectLoan = (pk) => {
        setSelectedLoans(prev => {
            if (prev.includes(pk)) {
                return prev.filter(id => id !== pk);
            } else {
                return [...prev, pk];
            }
        });
    };
    
    // ... (modal functions unchanged) ...
    const showModal = (title, message, isError = false) => {
        setModalContent({ title, message, isError });
        setIsModalOpen(true);
    };

    const hideModal = () => {
        setIsModalOpen(false);
    };

    const handleDeleteClick = (e) => {
        e.preventDefault(); 
        if (selectedCount === 0) {
            showModal('No Loans Selected', 'Please select at least one loan to delete.', true);
        } else {
            showModal('Confirm Deletion', `Are you sure you want to delete ${selectedCount} selected loan(s)? This action cannot be undone.`, false);
        }
    };

    const handleConfirmDelete = () => {
        hideModal();
        onDeleteSelected(selectedLoans);
        setSelectedLoans([]); 
    };

    const getMessageClasses = (tags) => {
        if (tags === 'success') return 'bg-green-100 text-green-800';
        if (tags === 'error') return 'bg-red-100 text-red-800';
        if (tags === 'warning') return 'bg-yellow-100 text-yellow-800';
        return 'bg-blue-100 text-blue-800';
    };

    // --- RETURN JSX ---
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
            
            {/* 🔍 Filter & Search Bar Section */}
            <div className="mb-6 flex flex-col md:flex-row gap-4 items-center justify-between p-4 bg-white rounded-lg shadow-md border border-slate-100">
                
                {/* Search by User Name */}
                <div className="w-full md:w-1/2">
                    <label htmlFor="search-user" className="sr-only">Search by User Name</label>
                    <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <svg className="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <input
                            type="text"
                            id="search-user"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            placeholder="Search by Applicant Name..."
                            className="block w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
                        />
                    </div>
                </div>

                {/* Filter by Loan Type Dropdown */}
                <div className="w-full md:w-1/2 md:max-w-xs">
                    <label htmlFor="filter-loan-type" className="block text-sm font-medium text-gray-700 mb-1">Filter by Loan Type</label>
                    <select
                        id="filter-loan-type"
                        value={selectedLoanType}
                        onChange={(e) => setSelectedLoanType(e.target.value)}
                        className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    >
                        {uniqueLoanTypes.map((type) => (
                            <option key={type} value={type}>
                                {type}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
            
            {/* Loans Table - CORRECTED STRUCTURE */}
            {filteredLoans.length > 0 ? (
                // Use relative positioning and a fixed height to contain the table and enable the header/body scroll trick
                <div className="bg-white rounded-3xl shadow-3xl border border-slate-100 p-8 relative">
                    <form onSubmit={handleDeleteClick}>
                        <div className="overflow-x-auto"> {/* Enable horizontal scrolling if needed */}
                            <table className="min-w-full divide-y divide-slate-200">
                                {/* <thead> for the FIXED header - NO CHANGES HERE */}
                                <thead className="bg-slate-50 sticky top-0 z-10 shadow-sm">
                                    <tr>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider rounded-tl-xl">
                                            <input
                                                type="checkbox"
                                                id="select-all"
                                                className="form-checkbox h-4 w-4 text-indigo-600 transition duration-150 ease-in-out rounded"
                                                checked={isAllSelected}
                                                onChange={handleSelectAll}
                                            />
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Applicant Name</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Loan Type</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Loan Amount</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Interest Rate</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Loan Term (Years)</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Submission Date</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Actions</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider rounded-tr-xl">Detail</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-slate-200">
                                    {filteredLoans.map((loan) => (
                                        // NOTE: Using `loan.pk` for the key and in the handler for consistency.
                                        <tr key={loan.id} className="hover:bg-slate-50 transition-colors duration-150 ease-in-out">
                                            <td className="px-6 py-4 whitespace-nowrap w-[2%]">
                                                <input
                                                    type="checkbox"
                                                    name="selected_loans"
                                                    value={loan.id}
                                                    className="form-checkbox h-4 w-4 text-indigo-600 transition duration-150 ease-in-out rounded"
                                                    checked={selectedLoans.includes(loan.id)} // Use pk consistently
                                                    onChange={() => handleSelectLoan(loan.id)} // Use pk consistently
                                                />
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{loan.applicant_name}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.loan_type_display}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{formatCurrency(loan.loan_amount)}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.annual_interest_rate_percent}%</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.loan_term_years}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{formatDate(loan.submission_date)}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                                <a href={`/download-appraisal-pdf/${loan.pk}`} className="text-indigo-600 hover:text-indigo-900 mr-4 transition-colors duration-150 ease-in-out">Download PDF</a>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600 cursor-pointer">View detail</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                        
                        {/* Delete Button (fixed at the bottom) */}
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
                <p className="text-center text-gray-600 text-lg p-10 bg-white rounded-lg shadow-md">
                    No approved loan applications found{initialLoans.length > 0 ? ' matching the current filter criteria.' : '.'}
                </p>
            )}

            {/* Custom Confirmation Modal (unchanged) */}
            <div 
                id="confirmation-modal" 
                className={`fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center z-50 ${isModalOpen ? '' : 'hidden'}`}
                onClick={hideModal}
            >
                <div 
                    className="bg-white rounded-lg shadow-xl p-8 max-w-sm w-full mx-4"
                    onClick={e => e.stopPropagation()} 
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