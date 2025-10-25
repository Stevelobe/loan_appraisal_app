import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeSalary = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Salary-Backed Specific Appraisal
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Field 1: Copy of Effective Service Document (File Upload) */}
        <FormField 
          name="copy_of_effective_service_document" 
          label="Copy of Effective Service Document" 
          type="file" 
          helpText="Upload proof of confirmed employment status."
        />

        {/* Field 2: Irrevocable Salary Transfer Document (File Upload) */}
        <FormField 
          name="irrevocable_salary_transfer_document" 
          label="Irrevocable Salary Transfer Document" 
          type="file" 
          helpText="Upload the signed commitment to transfer salary to the MFI."
        />
      </div>
      
      <div className="pt-4 space-y-3 border-t border-slate-200">
        <h4 className="text-xl font-semibold text-slate-800 pb-2">Required Checks</h4>
        
        {/* Checkbox 1: Salary Passing Union >= 3 Months */}
        <FormField 
            name="salary_passing_union_ge_3_months_check" 
            label="Salary has been passing through MFI for ≥ 3 months" 
            type="checkbox" 
            helpText="Internal check: Confirm salary history via MFI."
        />
        
        {/* Checkbox 2: Savings >= 1/10 of Loan */}
        <FormField 
            name="savings_ge_1_10_loan_check" 
            label="Savings balance is ≥ 1/10 of the requested loan amount" 
            type="checkbox" 
            helpText="Internal check: Confirm required mandatory savings deposit."
        />
      </div>
    </div>
  );
};

export default StepThreeSalary;