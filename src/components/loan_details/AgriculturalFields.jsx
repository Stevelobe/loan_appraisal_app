import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

// Define options for the loan purpose category dropdown
const purposeOptions = [
  { value: '', label: 'Select Loan Purpose Category' },
  { value: 'crops', label: 'Crops Production (Seasonal)' },
  { value: 'livestock', label: 'Livestock/Fishery' },
  { value: 'equipment', label: 'Farm Equipment/Infrastructure' },
  { value: 'other', label: 'Other Agricultural Use' },
];

const StepThreeAgricultural = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Agricultural Loan Specific Appraisal
      </h3>
      
      {/* Inputs and Document Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Dropdown: Loan Purpose Category */}
        <FormField 
          name="loan_purpose_category" 
          label="Loan Purpose Category" 
          type="select"
          options={purposeOptions}
          helpText="Specify the primary agricultural activity the loan will finance."
        />

        {/* Input Field: Savings Balance Amount */}
        <FormField 
          name="savings_balance_amount_agri" // Use a unique name to prevent collisions
          label="Current Savings Balance (XAF)" 
          type="number" 
          placeholder="e.g., 500000"
          helpText="Enter the member's current savings balance."
        />

        {/* File Upload: Total cost estimate of products and input */}
        <FormField 
          name="total_cost_estimate_document" 
          label="Total Cost Estimate Document" 
          type="file" 
          helpText="Upload the detailed budget for products and inputs."
        />
      </div>
      
      {/* Internal Checks Section */}
      <div className="pt-4 space-y-4 border-t border-slate-200">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Is the land a personal belonging */}
        <FormField 
            name="is_land_personal_belonging_check" 
            label="Agricultural land is verified as the borrower's personal property" 
            type="checkbox" 
            helpText="Verify land ownership for collateral assessment."
        />
        
        {/* Checkbox 2: Authorization of usage (conditionally required) */}
        <FormField 
            name="has_authorization_of_usage_check" 
            label="Authorization of land usage has been confirmed (if not owned by applicant)" 
            type="checkbox" 
            helpText="Required if the land is not the borrower's personal property."
        />

        {/* Checkbox 3: Savings balance must be 1/5 or 20% of the loan amount */}
        <FormField 
            name="savings_balance_ge_1_5_loan_check_agri" // Use a unique name
            label="Savings balance is ≥ 1/5 (20%) of the requested loan amount" 
            type="checkbox" 
            helpText="Confirm minimum savings balance requirement."
        />
        
        {/* Checkbox 4: Valid proof of source of income */}
        <FormField 
            name="valid_proof_of_source_of_income_check_agri" // Use a unique name
            label="Valid proof of non-farm source of income has been verified (if required)" 
            type="checkbox" 
            helpText="Confirm supplemental income for risk mitigation."
        />
      </div>
    </div>
  );
};

export default StepThreeAgricultural;