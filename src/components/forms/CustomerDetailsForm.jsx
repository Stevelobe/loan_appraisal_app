import React from 'react';
import InputField from '../InputField';
import { useFormContext } from 'react-hook-form';

const CustomerDetailsForm = () => {
  const { getValues } = useFormContext(); // To show the loan type

  return (
    <>
      <h2 className="text-xl font-bold mb-4">Customer Details for {getValues('loanType')}</h2>
      <p className="text-gray-600 mb-6">Please provide your contact information.</p>
      <InputField
        label="Full Name"
        name="customerName"
        placeholder="Enter your full name"
      />
      <InputField
        label="Email Address"
        name="customerEmail"
        type="email"
        placeholder="Enter your email"
      />
      <InputField
        label="Phone Number"
        name="customerPhone"
        type="tel"
        placeholder="e.g., +237 6XXXXXXXX"
      />
    </>
  );
};

export default CustomerDetailsForm;