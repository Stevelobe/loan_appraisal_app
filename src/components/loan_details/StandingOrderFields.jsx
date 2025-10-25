import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeStandingOrder = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Standing Order Loan Specific Checks
      </h3>
      
      <div className="space-y-4">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Standing Order Active >= 3 Months */}
        <FormField 
            name="standing_order_active_ge_3_months_check" 
            label="Standing Order has been active for ≥ 3 months" 
            type="checkbox" 
            helpText="Verify the consistency of the standing order payments."
        />
        
        {/* Checkbox 2: Loan Duration <= 1 Year */}
        <FormField 
            name="loan_duration_le_1_year_check" 
            label="Loan duration is ≤ 1 year (12 months)" 
            type="checkbox" 
            helpText="Confirm loan duration is within the approved short-term limit."
        />

        {/* Checkbox 3: Savings Balance >= 1/5 of Loan Requested */}
        <FormField 
            name="savings_balance_ge_1_5_loan_check" 
            label="Savings balance is ≥ 1/5 (20%) of the requested loan amount" 
            type="checkbox" 
            helpText="Confirm the required minimum savings balance for partial collateral."
        />
        
        {/* Checkbox 4: No Existing Default or Delinquency */}
        <FormField 
            name="no_existing_default_or_delinquency_check" 
            label="Applicant has no existing default or delinquency record" 
            type="checkbox" 
            helpText="Confirm the applicant's credit history is clean."
        />
      </div>
    </div>
  );
};

export default StepThreeStandingOrder;