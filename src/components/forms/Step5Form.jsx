import React from 'react';
import InputField from '../InputField';

const Step5Form = ({ formData, handleChange }) => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Verification</h2>
      <InputField
        label="Verification Code"
        name="verificationCode"
        placeholder="Enter verification code"
        value={formData.verificationCode}
        onChange={handleChange}
      />
      <p className="text-gray-600 text-sm mt-2">A verification code has been sent to your email/phone.</p>
    </>
  );
};

export default Step5Form;