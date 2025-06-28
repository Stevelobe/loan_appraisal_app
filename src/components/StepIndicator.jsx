import React from 'react';

const StepIndicator = ({ currentStep, steps }) => {
  return (
    <div className="mb-8 flex justify-between items-center relative">
      <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-200 -translate-y-1/2 z-0"></div>
      {steps.map((step, index) => (
        <div key={index} className="flex flex-col items-center z-10 w-1/3">
          <div
            className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white transition-colors duration-300
              ${index + 1 <= currentStep ? 'bg-blue-500' : 'bg-gray-400'}
            `}
          >
            {index + 1}
          </div>
          <div
            className={`text-sm mt-2 text-center transition-colors duration-300
              ${index + 1 <= currentStep ? 'text-blue-600 font-medium' : 'text-gray-500'}
            `}
          >
            {step}
          </div>
        </div>
      ))}
    </div>
  );
};

export default StepIndicator;