import React from 'react';
import InputField from '../InputField';

const Step4Form = ({ formData, handleChange }) => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Bank Information</h2>
      <InputField
        label="Bank Name"
        name="bankName"
        placeholder="Input bank name"
        value={formData.bankName}
        onChange={handleChange}
      />
      <InputField
        label="Account Number"
        name="accountNumber"
        placeholder="Input account number"
        value={formData.accountNumber}
        onChange={handleChange}
      />
      <InputField
        label="Routing Number"
        name="routingNumber"
        placeholder="Input routing number"
        value={formData.routingNumber}
        onChange={handleChange}
      />
    </>
  );
};

export default Step4Form;