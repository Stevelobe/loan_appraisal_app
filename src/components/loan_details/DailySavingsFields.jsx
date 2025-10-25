import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeDaily = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Daily Savings Loan Specific Appraisal
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Document 1: Signed Deduction Agreement from Daily Savings (File Upload) */}
        <FormField 
          name="signed_deduction_agreement_document" 
          label="Signed Deduction Agreement Document" 
          type="file" 
          helpText="Upload the agreement authorizing daily deductions for loan repayment."
        />

        {/* Document 2: Valid Surety Bond Document (File Upload) */}
        <FormField 
          name="valid_surety_bond_document" 
          label="Valid Surety Bond Document" 
          type="file" 
          helpText="Upload the document detailing the valid collateral or surety."
        />
      </div>
      
      <div className="pt-4 space-y-4 border-t border-slate-200">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Daily Savings Active for at Least 6 Months */}
        <FormField 
            name="daily_savings_active_ge_6_months_check" 
            label="Daily Savings account has been active for ≥ 6 months" 
            type="checkbox" 
            helpText="Verify the length and consistency of the savings history."
        />
        
        {/* Checkbox 2: Positive Loan Repayment History */}
        <FormField 
            name="positive_loan_repayment_history_check" 
            label="Applicant has a positive loan repayment history with the MFI" 
            type="checkbox" 
            helpText="Internal check: Confirm good standing on previous loans."
        />

        {/* Checkbox 3: Savings Balance >= 1/5 of Loan Requested */}
        <FormField 
            name="savings_balance_ge_1_5_loan_check" 
            label="Savings balance is ≥ 1/5 (20%) of the requested loan amount" 
            type="checkbox" 
            helpText="Confirm the required minimum savings balance for collateral."
        />
      </div>
    </div>
  );
};

export default StepThreeDaily;