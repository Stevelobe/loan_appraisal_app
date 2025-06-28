import React from 'react';
import InputField from '../InputField';

const Step2Form = ({ formData, handleChange }) => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">Location Information</h2>
      <InputField
        label="Location"
        name="location"
        placeholder="Input your location"
        value={formData.location}
        onChange={handleChange}
      />
    </>
  );
};

export default Step2Form;