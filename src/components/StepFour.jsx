// StepFour.jsx
import React from 'react';
import { useFormContext } from 'react-hook-form';
import { loanTypes } from '../loanTypeData'; // Assuming your loan types array is here

// Helper function to format the key for display
const formatLabel = (key) => {
  return key
    .replace(/_/g, ' ')
    .replace(/(?:^|\s)\S/g, (char) => char.toUpperCase());
};

const StepFour = () => {
  const { getValues } = useFormContext();
  const formData = getValues();
  
  // Get the display label for the selected loan type
  const selectedLoanLabel = loanTypes.find(t => t.value === formData.loan_type)?.label || 'N/A';

  // Determine which fields belong to which step/category (manual grouping for display)
  const stepOneFields = ['applicant_name', 'loan_amount', 'loan_duration', 'loan_type'];
  const stepTwoFields = ['identity_card_number', 'proof_of_address_document', 'bank_statement_document'];
  
  // All other fields are considered Step 3 specific fields
  const getStepThreeFields = (data) => {
    const allFields = Object.keys(data);
    return allFields.filter(key => 
      !stepOneFields.includes(key) && 
      !stepTwoFields.includes(key) &&
      data[key] !== undefined && // Filter out undefined fields
      data[key] !== '' &&
      data[key] !== null
    );
  };

  const stepThreeKeys = getStepThreeFields(formData);

  const displayValue = (value) => {
    if (typeof value === 'boolean') {
      return value ? '✅ Confirmed' : '❌ Not Confirmed';
    }
    if (value instanceof FileList) {
      return value.length > 0 ? value[0].name : 'No file uploaded';
    }
    return value || 'N/A';
  };

  return (
    <div className="space-y-8 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-indigo-700 border-b border-indigo-300 pb-3">
        Step 4: Final Review & Confirmation
      </h3>
      
      {/* --- 1. Applicant & Loan Info Review (Step 1) --- */}
      <div className="p-4 border rounded-lg bg-indigo-50/50 shadow-sm">
        <h4 className="text-xl font-semibold mb-3 text-slate-800">1. Applicant & Loan Info</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
          {stepOneFields.map(key => (
            <p key={key} className="text-sm">
              <strong className="text-slate-700">{formatLabel(key)}:</strong> 
              <span className="ml-2 font-medium">{key === 'loan_type' ? selectedLoanLabel : formData[key]}</span>
            </p>
          ))}
        </div>
      </div>

      {/* --- 2. KYC Details Review (Step 2) --- */}
      <div className="p-4 border rounded-lg bg-green-50/50 shadow-sm">
        <h4 className="text-xl font-semibold mb-3 text-slate-800">2. KYC Details</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
          {stepTwoFields.map(key => (
            <p key={key} className="text-sm">
              <strong className="text-slate-700">{formatLabel(key)}:</strong> 
              <span className="ml-2 font-medium">{displayValue(formData[key])}</span>
            </p>
          ))}
        </div>
      </div>

      {/* --- 3. Specific Loan Requirements Review (Step 3) --- */}
      <div className="p-4 border rounded-lg bg-yellow-50/50 shadow-sm">
        <h4 className="text-xl font-semibold mb-3 text-slate-800">3. Specific Loan Details ({selectedLoanLabel})</h4>
        {stepThreeKeys.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
            {stepThreeKeys.map(key => (
              <p key={key} className="text-sm">
                <strong className="text-slate-700">{formatLabel(key)}:</strong> 
                <span className="ml-2 font-medium">{displayValue(formData[key])}</span>
              </p>
            ))}
          </div>
        ) : (
          <p className="text-sm italic text-slate-600">No specific requirements entered for this loan type.</p>
        )}
      </div>
      
      <div className="mt-8">
        <button 
          type="submit" 
          className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-xl shadow-lg focus:outline-none transition-all duration-300 ease-in-out flex items-center justify-center text-lg tracking-wide"
        >
          <span className="mr-2 text-2xl">✅</span> Final Submit Application
        </button>
      </div>
    </div>
  );
};
export default StepFour;