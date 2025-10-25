// StepThree.jsx
import React from 'react';
import { useFormContext } from 'react-hook-form';

// Import all 7 specific field components
import MortgageFields from './loan_details/MortgageFields';
import SalaryBackedFields from './loan_details/SalaryBackedFields';
import LoanWithinSavingsFields from './loan_details/LoanWithinSavingsFields';
import DailySavingsFields from './loan_details/DailySavingsFields';
import StandingOrderFields from './loan_details/StandingOrderFields';
import RealEstateFields from './loan_details/RealEstateFields';
import ContainerFields from './loan_details/ContainerFields';

// Map the loan type value (from Step 1) to the component
const LoanFieldsMap = {
  'mortgage-loan': MortgageFields,
  'salary-backed-loan': SalaryBackedFields,
  'loan-within-savings': LoanWithinSavingsFields,
  'daily-savings-loan': DailySavingsFields,
  'standing-order-loan': StandingOrderFields,
  'real-estate-loan': RealEstateFields,
  'container-loan': ContainerFields,
};

const StepThree = () => {
  // We use watch to get the selected loan type from Step 1
  const { watch } = useFormContext();
  const selectedLoanType = watch('loan_type'); 

  // Dynamically get the correct component to render
  const SpecificLoanFields = LoanFieldsMap[selectedLoanType];

  if (!selectedLoanType) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
        Please select a Loan Type in Step 1 to continue.
      </div>
    );
  }

  return (
    <div className="space-y-4 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Specific Loan Details and Documents
      </h3>
      {SpecificLoanFields ? (
        // Render the component for the specific loan type
        <SpecificLoanFields />
      ) : (
        <p className="p-4 bg-yellow-50 border border-yellow-200 text-yellow-700 rounded-md">
          No specific form details defined for the selected loan type: **{selectedLoanType}**.
        </p>
      )}
    </div>
  );
};
export default StepThree;