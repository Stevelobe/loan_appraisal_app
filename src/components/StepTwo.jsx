import React from 'react';
import { useFormContext } from 'react-hook-form';
import { FormField } from './StepOne'; // Reusing the Field component from StepOne

const StepTwo = () => {
  return (
    <div className="space-y-6 pt-6 border-t border-slate-200">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 2: KYC Details
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <FormField name="identity_card_number" label="Identity Card Number" />
        <FormField name="date_of_birth" label="Date of Birth" type="date" />

        <FormField name="place_of_birth" label="Place of Birth" />
        <FormField name="current_address" label="Current Address" helpText="Full street address, city, and country." />

        <FormField name="marital_status" label="Marital Status" type="select">
            {/* Hardcode a simple select for demo */}
            <option value="">Select Status</option>
            <option value="Single">Single</option>
            <option value="Married">Married</option>
            <option value="Divorced">Divorced</option>
            <option value="Widowed">Widowed</option>
        </FormField>
        <FormField name="profession" label="Profession/Occupation" />

        <FormField name="duration_with_mfi_years" label="Duration with MFI (Years)" type="number" helpText="How long the applicant has been a member/client." />
        <FormField name="num_loans_other_mfi" label="No. of Loans from Other MFIs" type="number" />
        
        <FormField name="current_location" label="Current Location (City/Town)" />
      </div>
    </div>
  );
};

export default StepTwo;