import React from 'react';

const StepIndicator = ({ currentStep, steps }) => {
  return (
    <div className="flex justify-between items-center mb-10 relative">
      <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-gray-300 transform -translate-y-1/2 mx-8"></div>
      {steps.map((stepName, index) => (
        <div key={index} className="flex flex-col items-center z-10">
          <div
            className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold
              ${index + 1 <= currentStep ? 'bg-green-500' : 'bg-gray-400'}`}
          >
            {index + 1}
          </div>
          <span className={`mt-2 text-sm ${index + 1 <= currentStep ? 'text-green-600' : 'text-gray-600'}`}>
            {stepName}
          </span>
        </div>
      ))}
    </div>
  );
};

export default StepIndicator;