import React from 'react';
import InputField from '../InputField';
import SelectField from '../SelectField';

const Step3Form = ({ formData, handleChange }) => {
  return (
    <>
      <h2 className="text-xl font-bold mb-4">BUSINESS INFORMATION</h2>
      <p className="text-gray-600 mb-6">Provide the necessary details to register your business with us</p>
      <InputField
        label="Business Name"
        name="businessName"
        placeholder="Input business name"
        value={formData.businessName}
        onChange={handleChange}
      />
      <InputField
        label="Business Owner"
        name="businessOwner"
        placeholder="Input first and last name"
        value={formData.businessOwner}
        onChange={handleChange}
      />
      <SelectField
        label="Business Type"
        name="businessType"
        options={[
          { value: '', label: 'Select from list' },
          { value: 'Retail', label: 'Retail' },
          { value: 'Service', label: 'Service' },
          { value: 'Manufacturing', label: 'Manufacturing' },
        ]}
        value={formData.businessType}
        onChange={handleChange}
      />
      <InputField
        label="Identification Number"
        name="identificationNumber"
        placeholder="Input business's identification number"
        value={formData.identificationNumber}
        onChange={handleChange}
      />
    </>
  );
};

export default Step3Form;