import React from 'react';
import InputField from '../../InputField';

const MortgageLoanDetailsForm = () => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Loan Details: Mortgage Loans</h2>
      <p className="text-gray-600 mb-6">Provide property details for your mortgage loan application.</p>
      <InputField
        label="Property Address"
        name="propertyAddress"
        placeholder="Enter the full property address"
      />
      <InputField
        label="Property Market Value (CFA)"
        name="propertyMarketValue"
        type="number"
        placeholder="e.g., 25000000"
      />
      <InputField
        label="Loan Amount Requested (CFA)"
        name="loanAmountRequested"
        type="number"
        placeholder="e.g., 20000000"
      />
      <InputField
        label="Property Description"
        name="propertyDescription"
        type="textarea" // Using type="textarea" for a textarea input
        placeholder="Briefly describe the property (e.g., type, number of rooms, condition)"
      />
    </>
  );
};

export default MortgageLoanDetailsForm;