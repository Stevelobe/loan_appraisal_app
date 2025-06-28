import React from 'react';
import InputField from '../../InputField';

const SalaryLoanDetailsForm = () => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Loan Details: Loans Covered by Salary</h2>
      <p className="text-gray-600 mb-6">Provide your salary and employment details for this loan type.</p>
      <InputField
        label="Monthly Salary (CFA)"
        name="monthlySalary"
        type="number"
        placeholder="e.g., 300000"
      />
      <InputField
        label="Loan Amount Requested (CFA)"
        name="loanAmountRequested"
        type="number"
        placeholder="e.g., 900000"
      />
      <InputField
        label="Employer Name"
        name="employerName"
        placeholder="Enter your employer's name"
      />
      <InputField
        label="Employment Start Date"
        name="employmentStartDate"
        type="date"
      />
    </>
  );
};

export default SalaryLoanDetailsForm;