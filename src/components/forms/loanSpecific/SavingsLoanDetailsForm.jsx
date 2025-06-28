import React from 'react';
import InputField from '../../InputField';

const SavingsLoanDetailsForm = () => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Loan Details: Loans within Savings</h2>
      <p className="text-gray-600 mb-6">Provide your current savings balance and desired loan amount.</p>
      <InputField
        label="Current Savings Balance (CFA)"
        name="savingsBalance"
        type="number"
        placeholder="e.g., 500000"
      />
      <InputField
        label="Loan Amount Requested (CFA)"
        name="loanAmountRequested"
        type="number"
        placeholder="e.g., 200000"
      />
    </>
  );
};

export default SavingsLoanDetailsForm;