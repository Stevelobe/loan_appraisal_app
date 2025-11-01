import React from 'react';
import { FormField } from '../StepOne'; // Reusing the FormField component

const StepThreeMortgage = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 3: Mortgage-Specific Appraisal
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Field 2: Supporting Documents (Textarea for notes/list) */}
        <div className="md:col-span-2">
            <FormField 
              name="supporting_documents" 
              label="Supporting Documents/Notes" 
              type="textarea" // Note: FormField will need a small update for textarea
              helpText="List any additional supporting documents or appraisal notes."
            />
        </div>
      </div>
      
      <div className="pt-4 space-y-3">
        <h4 className="text-xl font-semibold text-slate-800 border-b border-slate-300 pb-2">Required Checks</h4>
        <FormField 
          name="legal_mortgage_agreement_document" 
          label="Legal Mortgage Agreement Document" 
          type="checkbox" 
          helpText="Is the signed legal agreement document valid ?"
        />
        
        {/* Checkbox 1: Land Title Document */}
        <FormField 
            name="land_title_document" 
            label="Land Title Document Confirmed" 
            type="checkbox" 
            helpText="Verify the land title document is valid and clear."
        />
        
        {/* Checkbox 2: Power of Attorney Document */}
        <FormField 
            name="power_of_attorney_document" 
            label="Power of Attorney Document Confirmed" 
            type="checkbox" 
            helpText="Confirm power of attorney documents (if applicable) are in order."
        />

        {/* Checkbox 3: No Existing NPL */}
        <FormField 
            name="no_existing_npl" 
            label="No Existing Non-Performing Loan (NPL) Record" 
            type="checkbox" 
            helpText="Confirm applicant has no record of existing Non-Performing Loans."
        />
      </div>
    </div>
  );
};

export default StepThreeMortgage;