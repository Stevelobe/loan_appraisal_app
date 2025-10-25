import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeContainer = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Container Loan Specific Appraisal
      </h3>
      
      {/* Document and Data Entry Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* File Upload 1: Copy of Bill of Lading */}
        <FormField 
          name="bill_of_lading_document" 
          label="Copy of Bill of Lading" 
          type="file" 
          helpText="Upload the shipping document proving ownership and transport."
        />

        {/* File Upload 2: Custom Clearance Plan */}
        <FormField 
          name="custom_clearance_plan_document" 
          label="Custom Clearance Plan Document" 
          type="file" 
          helpText="Upload the plan detailing the customs clearance process."
        />

        {/* Input Field: Savings Balance Amount */}
        <FormField 
          name="savings_balance_amount" 
          label="Current Savings Balance (XAF)" 
          type="number" 
          placeholder="e.g., 200000"
          helpText="Enter the member's current savings balance for verification."
        />
      </div>
      
      {/* Internal Checks Section */}
      <div className="pt-4 space-y-4 border-t border-slate-200">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Savings Balance >= 1/5 of Loan Requested */}
        <FormField 
            name="savings_balance_ge_1_5_loan_check" 
            label="Savings balance is ≥ 1/5 (20%) of the requested loan amount" 
            type="checkbox" 
            helpText="Confirm the required minimum savings balance for collateral."
        />
        
        {/* Checkbox 2: Valid Proof of Source of Income */}
        <FormField 
            name="valid_proof_of_source_of_income_check_container" 
            label="Valid proof of source of income has been verified" 
            type="checkbox" 
            helpText="Confirm the ability of the borrower to service the loan."
        />

        {/* Important Note */}
        <div className="p-4 bg-yellow-50 border-l-4 border-yellow-500 text-yellow-800 rounded-md shadow-sm">
            <p className="font-semibold text-sm">Important Note:</p>
            <p className="text-sm">For Container Loans above 10,000,000 XAF, a legal mortgage is highly recommended.</p>
        </div>
      </div>
    </div>
  );
};

export default StepThreeContainer;