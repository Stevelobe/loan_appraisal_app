import React from 'react';
import { useFormContext } from 'react-hook-form';
const FormField = ({ name, label, type = 'text', helpText,options=[], ...props }) => {
  const { register, formState: { errors } } = useFormContext();
  const error = errors[name];

  // Base Tailwind classes for input/select/textarea
  const baseClass = "mt-1 block w-full pl-3 pr-4 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md shadow-sm";
  const checkboxClass = "h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500";
  const errorClass = error ? "border-red-500 ring-red-500" : "";
  const fileClass = "block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100";
  
  // Helper for input type
  const renderInput = () => {
      if (type === 'select') {
            return (
                <select 
                    id={name} 
                    {...register(name)} 
                    className={`${baseClass} ${errorClass}`}
                    {...props}
                >
                    {/* 1. Default/Placeholder Option */}
                    <option value="">Select an Option</option>
                    
                    {/* 2. Dynamically Render Options using the passed 'options' prop */}
                    {options.map((option) => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}

                    {/* REMOVED: The hardcoded options (Personal, Business, Other) are gone. */}
                </select>
            );
        }
      
      if (type === 'textarea') {
          return (
              <textarea
                  id={name}
                  rows={4}
                  {...register(name)}
                  className={`${baseClass} ${errorClass}`}
                  {...props}
              />
          );
      }

      if (type === 'checkbox') {
        // Special rendering for checkbox to align label and input
        return (
            <div className="flex items-center space-x-3">
                <input
                    id={name}
                    type="checkbox"
                    {...register(name)}
                    className={checkboxClass}
                    {...props}
                />
                <label htmlFor={name} className="text-base font-semibold text-slate-700 cursor-pointer">
                    {label}
                </label>
            </div>
        );
      }

      if (type === 'file') {
        return (
          <input
              id={name}
              type="file"
              // Note: react-hook-form handles file uploads using register, but valueAsNumber must be false/undefined
              {...register(name)} 
              className={`${fileClass}`}
              {...props}
          />
        );
      }

      // Default to input (text, number, date, email, etc.)
      return (
          <input
              id={name}
              type={type}
              {...register(name, { valueAsNumber: type === 'number' || type === 'date' ? false : undefined })}
              className={`${baseClass} ${errorClass}`}
              {...props}
          />
      );
  };
  
  // Special handling for Checkbox Wrapper (removes the top label if it's a checkbox)
  if (type === 'checkbox') {
    return (
        <div className="field-wrapper">
            {renderInput()}
            {helpText && <p className="mt-2 text-sm text-slate-500 pl-7">{helpText}</p>}
            {error && (
              <p className="mt-2 text-sm text-red-600 font-medium flex items-center pl-7">
                <span className="mr-1.5 text-lg">⚠️</span> {error.message}
              </p>
            )}
        </div>
    );
  }

  // Default Wrapper
  return (
    <div className="field-wrapper">
      <label htmlFor={name} className="block text-base font-semibold text-slate-700 mb-2">
        {label}
      </label>
      {renderInput()}
      {helpText && <p className="mt-2 text-sm text-slate-500">{helpText}</p>}
      {error && (
        <p className="mt-2 text-sm text-red-600 font-medium flex items-center">
          <span className="mr-1.5 text-lg">⚠️</span> {error.message}
        </p>
      )}
    </div>
  );
};

const purposeOptions = [
  { value: '', label: 'Select A Loan Purpose' },
  { value: 'business', label: 'Business' },
  { value: 'personal', label: 'Personal' },
  { value: 'other', label: 'other' },
];
const StepOne = () => {
  return (
    <div className="space-y-6">
      <h3 className="text-2xl font-bold text-slate-800 border-b border-slate-300 pb-3">
        Step 1: Applicant & Loan Info
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField name="applicant_name" label="Applicant Name" />
          <FormField name="applicant_email" label="Applicant Email" type="email" />
          
          <FormField name="loan_amount" label="Loan Amount (XAF)" type="number" helpText="Requested principal amount." />
          <FormField name="annual_interest_rate_percent" label="Annual Interest Rate (%)" type="number" />
          
          <FormField name="loan_term_years" label="Loan Term (Years)" type="number" />
          <FormField name="borrower_gross_monthly_income" label="Gross Monthly Income (XAF)" type="number" helpText="Total income before deductions." />
          
          <FormField name="existing_monthly_debt_payments" label="Existing Monthly Debt Payments (XAF)" type="number" helpText="Total monthly payments on other loans/debt." />
          <FormField name="account_number" label="Account Number" />

          <FormField name="date_of_loan" label="Date of Loan Application" type="date" />
          <FormField name="loan_purpose" label="Loan Purpose" type="select" options={purposeOptions}>
              {/* Options will be inside the FormField select block, as shown in its implementation */}
          </FormField>
      </div>
    </div>
  );
};

export {FormField, StepOne};