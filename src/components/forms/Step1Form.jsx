import React from 'react';
import InputField from '../InputField';

const Step1Form = ({ formData, handleChange }) => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">User Name Information</h2>
      <InputField
        label="User Name"
        name="username"
        placeholder="Input your user name"
        value={formData.username}
        onChange={handleChange}
      />
      <InputField
        label="User Name"
        name="username"
        placeholder="Input your user name"
        value={formData.username}
        onChange={handleChange}
      />
    </>
  );
};

export default Step1Form;