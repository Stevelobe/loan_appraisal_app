import React from 'react';
import { useFormContext } from 'react-hook-form';

const InputField = ({ label, type = 'text', placeholder, name }) => {
  const { register, formState: { errors } } = useFormContext();
  const errorMessage = errors[name]?.message;

  const InputComponent = type === 'textarea' ? 'textarea' : 'input';

  return (
    <div className="mb-4">
      <label htmlFor={name} className="block text-gray-700 text-sm font-bold mb-2">
        {label}
      </label>
      <InputComponent
        type={type !== 'textarea' ? type : undefined} // Only pass type for input, not for textarea
        id={name}
        {...register(name, { valueAsNumber: type === 'number' })} // Register with valueAsNumber for number type
        className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${errorMessage ? 'border-red-500' : ''}`}
        placeholder={placeholder}
        rows={type === 'textarea' ? 4 : undefined} // Add rows for textarea
      />
      {errorMessage && (
        <p className="text-red-500 text-xs italic mt-1">{errorMessage}</p>
      )}
    </div>
  );
};

export default InputField;