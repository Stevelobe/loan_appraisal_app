import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeRealEstate = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Real Estate Specific Appraisal
      </h3>
      
      {/* Document Upload Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* File Upload: Legal Mortgage Agreement signed */}
        <FormField 
          name="legal_mortgage_agreement_document_re" 
          label="Signed Legal Mortgage Agreement Document" 
          type="file" 
          helpText="Upload the signed agreement documenting the mortgage."
        />
      </div>
      
      {/* Internal Checks Section */}
      <div className="pt-4 space-y-4 border-t border-slate-200">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Loan Duration >= 10 Years */}
        <FormField 
            name="loan_duration_ge_10_years_check" 
            label="Loan duration is specified as ≥ 10 years" 
            type="checkbox" 
            helpText="Confirm this long-term loan meets the minimum duration requirement."
        />
        
        {/* Checkbox 2: Loan Amount <= 10% Paid-Up Capital */}
        <FormField 
            name="loan_amount_le_10_percent_paid_up_capital_check" 
            label="Loan amount is ≤ 10% of MFI's Paid-Up Capital" 
            type="checkbox" 
            helpText="Internal regulatory check for maximum lending exposure."
        />

        {/* Checkbox 3: Land Title in Borrower's Name */}
        <FormField 
            name="land_title_in_borrowers_name_check" 
            label="Land title is registered directly in the borrower's name" 
            type="checkbox" 
            helpText="Confirm clear legal ownership for collateral."
        />
        
        {/* Checkbox 4: Valid Proof of Source of Income */}
        <FormField 
            name="valid_proof_of_source_of_income_check" 
            label="Valid proof of source of income has been verified" 
            type="checkbox" 
            helpText="Confirm the ability of the borrower to repay the loan."
        />
      </div>
    </div>
  );
};

export default StepThreeRealEstate;