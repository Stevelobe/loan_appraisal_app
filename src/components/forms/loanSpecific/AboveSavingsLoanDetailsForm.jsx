import React from 'react';
import InputField from '../../InputField';

const AboveSavingsLoanDetailsForm = () => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Loan Details: Loans Above Savings</h2>
      <p className="text-gray-600 mb-6">Provide your current savings balance, desired loan amount, and details of additional guarantees.</p>
      <InputField
        label="Current Savings Balance (CFA)"
        name="savingsBalance"
        type="number"
        placeholder="e.g., 100000"
      />
      <InputField
        label="Loan Amount Requested (CFA)"
        name="loanAmountRequested"
        type="number"
        placeholder="e.g., 500000"
      />
      <InputField
        label="Guarantees/Collateral Description"
        name="guaranteesDescription"
        type="textarea" // Using type="textarea" for a textarea input
        placeholder="Describe any additional guarantees or collateral (e.g., vehicle, property, co-signer)"
      />
    </>
  );
};

export default AboveSavingsLoanDetailsForm;