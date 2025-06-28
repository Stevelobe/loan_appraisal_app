// src/components/forms/SummaryForm.jsx

import React from 'react';
import { useFormContext } from 'react-hook-form';
import { loanTypeConfig } from '../../utils/loanSchemas'; // Import loanTypeConfig

const SummaryForm = ({ loanType }) => { // Accept loanType as a prop
  const { getValues } = useFormContext();
  const formData = getValues(); // Get all form data

  // Determine relevant fields based on loanTypeConfig
  const relevantFields = loanTypeConfig[loanType]?.relevantFields || [];
  // Always include 'loanType' itself, as it's set in defaultValues
  const fieldsToShow = new Set([...relevantFields, 'loanType']);

  // Utility function to format field names for display
  const formatFieldName = (fieldName) => {
    return fieldName
      .replace(/([A-Z])/g, ' $1') // Add space before capital letters
      .replace(/^./, (str) => str.toUpperCase()); // Capitalize the first letter
  };

  return (
    <>
      <h2 className="text-xl font-bold mb-4">Review Your Loan Application</h2>
      <p className="text-gray-600 mb-6">Please review all the details before submitting your application.</p>

      <div className="bg-gray-50 p-4 rounded-lg shadow-inner mb-6">
        {Object.entries(formData).map(([key, value]) => {
          // Only show field if it's relevant AND has a non-empty/non-null value
          if (fieldsToShow.has(key) && (value !== '' && value !== null && typeof value !== 'undefined' && value !== 0)) {
            let displayValue = value;
            if (typeof value === 'object' && value instanceof Date) {
              displayValue = value.toLocaleDateString(); // Format dates nicely
            } else if (typeof value === 'number') {
              displayValue = value.toLocaleString(); // Format numbers with commas
            } else if (typeof value === 'string' && value.startsWith('http')) {
              displayValue = <a href={value} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Link</a>;
            }

            return (
              <div key={key} className="mb-2">
                <span className="font-semibold text-gray-700">{formatFieldName(key)}:</span>{' '}
                <span className="text-gray-900">{displayValue}</span>
              </div>
            );
          }
          return null; // Don't render irrelevant or empty fields
        })}
        {fieldsToShow.size === 1 && formData.loanType && ( // Only loanType is shown implies no other relevant fields were filled
            <p className="text-gray-500 italic">No specific loan details entered yet, or selected loan type has minimal fields.</p>
        )}
      </div>

      <p className="text-blue-600 text-sm italic">
        Ensure all information is accurate before final submission.
      </p>
    </>
  );
};

export default SummaryForm;