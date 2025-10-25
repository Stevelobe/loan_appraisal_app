import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeBusiness = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Business Loan Specific Details & Documents
      </h3>
      
      {/* Document Upload Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* File Upload 1: Business Registration Document */}
        <FormField 
          name="business_registration_document" 
          label="Business Registration Certificate/ID" 
          type="file" 
          helpText="Upload the official document proving business entity status."
        />

        {/* File Upload 2: Last 3 Years Financial Statements */}
        <FormField 
          name="financial_statements_document" 
          label="Last 3 Years Financial Statements" 
          type="file" 
          helpText="Upload income statements, balance sheets, or similar documents."
        />

        {/* File Upload 3: Detailed Business Plan */}
        <FormField 
          name="business_plan_document" 
          label="Detailed Business Plan" 
          type="file" 
          helpText="Upload the plan detailing market, strategy, and projections."
        />
      </div>
      
      {/* Internal Checks Section */}
      <div className="pt-4 space-y-4 border-t border-slate-200">
        <h4 className="text-xl font-semibold text-slate-700 pb-2">Internal Confirmation Checks</h4>
        
        {/* Checkbox 1: Business operational for min 3 years */}
        <FormField 
            name="business_operational_min_3_years_check" 
            label="Business has been verifiably operational for a minimum of 3 years" 
            type="checkbox" 
            helpText="Confirm long-term stability and operational history."
        />
        
        {/* Checkbox 2: Adequate collateral assessed */}
        <FormField 
            name="adequate_collateral_assessed_check" 
            label="Adequate collateral has been independently assessed and verified" 
            type="checkbox" 
            helpText="Confirm security arrangements for the business loan."
        />
      </div>
    </div>
  );
};

export default StepThreeBusiness;