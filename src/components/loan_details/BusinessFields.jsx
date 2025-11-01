import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeBusiness = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Business Loan Specific Details & Documents
      </h3>
      
      {/* Internal Checks Section */}
      <div className="pt-4 space-y-4 border-t border-slate-200">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: valid_source_of_income_for_repayment */}
        <FormField 
            name="valid_source_of_income_for_repayment" 
            label="Valid source of income for repayment" 
            type="checkbox" 
            helpText="Confirm valid source of income for repayment"
        />
        
        {/* Checkbox 2: land_documents_attached */}
        <FormField 
            name="land_documents_attached" 
            label="Adequate collateral has been independently assessed and verified" 
            type="checkbox" 
            helpText="Confirm security arrangements for the business loan."
        />

        {/* Checkbox 3: Confirmin saving balance */}
        <FormField 
            name="savings_balance_ge_20_percent_loan" 
            label="Confirmin saving balance" 
            type="checkbox" 
            helpText="Confirm that the saving balance is greater or equal to 20% of loan amount"
        />

        {/* Checkbox 4: cost_estimate_provided */}
        <FormField 
            name="cost_estimate_provided" 
            label="Confirm cost estimate provided" 
            type="checkbox" 
            helpText="Confirm cost estimate provided"
        />
      </div>
    </div>
  );
};

export default StepThreeBusiness;