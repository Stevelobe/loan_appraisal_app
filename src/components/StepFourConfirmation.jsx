import React from 'react';
import { useFormContext } from 'react-hook-form'; // <-- Use RHF context

// Helper function to format field names for display (e.g., 'full_name' -> 'Full Name')
const formatLabel = (name) => {
    return name
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
        // Clean up loan type specific field suffixes
        .replace(/ Re| Agri| Container| Express| Business/g, ''); 
};

// Helper function to render the value cleanly
const renderValue = (value) => {
    if (value === true) return <span className="text-green-600 font-bold">Confirmed / Yes ✅</span>;
    if (value === false) return <span className="text-red-600 font-bold">Not Confirmed / No ❌</span>;
    if (value instanceof File) return <span className="text-indigo-600 font-medium">{value.name} (File ready for upload) 📄</span>;
    if (typeof value === 'number') return value.toLocaleString('en-US', { minimumFractionDigits: 0 }) + " XAF"; 
    if (!value) return <span className="text-slate-500 italic">N/A or Not Provided</span>;
    return String(value);
};

const StepFourConfirmation = () => {
    // Get form methods and values from the parent FormProvider
    const { getValues, formState: { errors } } = useFormContext();
    const values = getValues(); 
    
    // Determine the loan type
    // Note: Assuming 'selectedLoanType' is stored in the root of the form data
    const loanType = values.selectedLoanType || 'unknown-loan'; 

    // --- Field Grouping ---
    // Define the exact keys for the first two steps based on your schema
    const stepOneFields = ['applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent', 'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments', 'account_number', 'date_of_loan', 'loan_purpose'];
    const stepTwoFields = ['identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession', 'current_location'];
    
    // Filter out step 1 and 2 keys to get the dynamic Step 3 fields
    const filteredValues = Object.entries(values).filter(([key]) => 
        !stepOneFields.includes(key) && !stepTwoFields.includes(key) && key !== 'selectedLoanType'
    );
    const stepThreeKeys = filteredValues.map(([key]) => key);

    const hasErrors = Object.keys(errors).length > 0;

    return (
        <div className="space-y-8 pt-6 border-t border-slate-200">
            <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
                Step 4: Review & Final Submission
            </h3>

            {/* Loan Type Header */}
            <div className="p-4 bg-indigo-50 border-l-4 border-indigo-400 text-indigo-800 rounded-md shadow-sm">
                <p className="text-lg font-semibold">Loan Type Selected:</p>
                <p className="text-xl font-extrabold capitalize">{loanType.replace(/-/g, ' ')}</p>
            </div>
            
            {hasErrors && (
                <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg font-semibold">
                    ⚠️ Please correct the errors in the previous steps before submission.
                </div>
            )}

            {/* Summary Sections */}
            {[
                { title: "Step 1: Applicant & Loan Details", keys: stepOneFields },
                { title: "Step 2: KYC Details", keys: stepTwoFields },
                { title: `Step 3: ${loanType.replace(/-/g, ' ').toUpperCase()} Specifics`, keys: stepThreeKeys }
            ].map(({ title, keys }) => (
                <div key={title} className="bg-white p-6 rounded-xl shadow-lg border border-slate-100">
                    <h4 className="text-xl font-bold text-slate-700 mb-4 pb-2 border-b border-slate-200">{title}</h4>
                    <dl className="space-y-3">
                        {keys.map(key => {
                            const value = values[key];
                            if (value !== undefined && value !== null) {
                                return (
                                    <div key={key} className="grid grid-cols-3 gap-4">
                                        <dt className="text-sm font-semibold text-slate-500">{formatLabel(key)}:</dt>
                                        <dd className="col-span-2 text-base font-medium text-slate-800 break-words">
                                            {renderValue(value)}
                                        </dd>
                                    </div>
                                );
                            }
                            return null;
                        })}
                    </dl>
                </div>
            ))}
        </div>
    );
};

export default StepFourConfirmation;