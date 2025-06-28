import React from 'react';
import InputField from '../../InputField';

const StandingOrderLoanDetailsForm = () => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Loan Details: Loans Covered by Standing Order</h2>
      <p className="text-gray-600 mb-6">Provide details about your fixed income source and existing financial obligations.</p>
      <InputField
        label="Fixed Income Source Description"
        name="fixedIncomeSourceDescription"
        placeholder="e.g., Monthly pension, Rental income"
      />
      <InputField
        label="Monthly Fixed Income Amount (CFA)"
        name="monthlyFixedIncomeAmount"
        type="number"
        placeholder="e.g., 150000"
      />
      <InputField
        label="Loan Amount Requested (CFA)"
        name="loanAmountRequested"
        type="number"
        placeholder="e.g., 400000"
      />
      <InputField
        label="Existing Financial Obligations"
        name="existingFinancialObligations"
        type="textarea" // Using type="textarea" for a textarea input
        placeholder="List any other ongoing loan payments, debts, etc."
      />
    </>
  );
};

export default StandingOrderLoanDetailsForm;