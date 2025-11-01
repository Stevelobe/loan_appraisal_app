import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeSavings = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Loan Within Savings Specific Checks
      </h3>
      
      <div className="space-y-4">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Savings Covers Loan Plus Interest */}
        <FormField 
            name="savings_covers_loan_plus_interest" 
            label="Savings balance fully covers the requested loan amount PLUS interest" 
            type="checkbox" 
            helpText="This is the primary security check for this loan type."
        />
        
        {/* Checkbox 2: Loan Amount Blocked in Savings */}
        <FormField 
            name="loan_amount_blocked_in_savings" 
            label="Loan principal amount has been blocked in the member's savings account" 
            type="checkbox" 
            helpText="Confirm a hold has been placed on the necessary savings amount."
        />

        {/* Checkbox 3: No Active Default */}
        <FormField 
            name="no_active_default" 
            label="Applicant has no active default record with the MFI" 
            type="checkbox" 
            helpText="Confirm the applicant is in good standing before approval."
        />
      </div>
    </div>
  );
};

export default StepThreeSavings;