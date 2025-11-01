import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeExpress = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Express Loan Specific Checks
      </h3>
      
      {/* Internal Checks Section */}
      <div className="space-y-4">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Salary deducted at source or standing order available */}
        <FormField 
            name="salary_deducted_at_source_or_standing_order" 
            label="Salary deduction at source or standing order for repayment is confirmed" 
            type="checkbox" 
            helpText="Verify the automated mechanism for loan repayment."
        />
        
        {/* Checkbox 2: Effective service available */}
        <FormField 
            name="effective_service_available" 
            label="Applicant has an 'effective service' (e.g., active account history) available" 
            type="checkbox" 
            helpText="Confirm the applicant's account history meets the service criteria."
        />

        {/* Checkbox 3: Is there a clearly/valid purpose of loan */}
        <FormField 
            name="clearly_valid_purpose_of_loan" 
            label="Loan has a clearly defined and valid purpose" 
            type="checkbox" 
            helpText="Confirm the intended use of the funds is acceptable."
        />
        
        {/* Checkbox 4: Savings balance must be 1/10 or 10% of loan amount */}
        <FormField 
            name="savings_balance_ge_1_10_loan" 
            label="Savings balance is ≥ 1/10 (10%) of the requested loan amount" 
            type="checkbox" 
            helpText="Confirm the required minimum savings balance for express collateral."
        />

        {/* Checkbox 5: No existing delinquent loan */}
        <FormField 
            name="no_existing_delinquent_loan" 
            label="Applicant has no existing delinquent loans" 
            type="checkbox" 
            helpText="Confirm the applicant's recent credit repayment status."
        />
      </div>

      {/* Data Entry Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-200">
        {/* Text Field: Savings Balance Amount */}
        <FormField 
          name="savings_balance_amount" 
          label="Current Savings Balance (XAF)" 
          type="number" 
          placeholder="e.g., 50000"
          helpText="Enter the member's current savings balance for verification."
        />
      </div>
    </div>
  );
};

export default StepThreeExpress;