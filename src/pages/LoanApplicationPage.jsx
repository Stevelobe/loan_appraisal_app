// src/pages/LoanApplicationPage.jsx

import React, { useState, useCallback, useEffect } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { useParams } from 'react-router-dom';

import StepIndicator from '../components/StepIndicator';
import CustomerDetailsForm from '../components/forms/CustomerDetailsForm';
import SummaryForm from '../components/forms/SummaryForm';

// Loan-specific detail forms
import SavingsLoanDetailsForm from '../components/forms/loanSpecific/SavingsLoanDetailsForm';
import AboveSavingsLoanDetailsForm from '../components/forms/loanSpecific/AboveSavingsLoanDetailsForm';
import SalaryLoanDetailsForm from '../components/forms/loanSpecific/SalaryLoanDetailsForm';
import StandingOrderLoanDetailsForm from '../components/forms/loanSpecific/StandingOrderLoanDetailsForm';
import MortgageLoanDetailsForm from '../components/forms/loanSpecific/MortgageLoanDetailsForm';

// Import schemas and config from utility file
import {
  customerDetailsSchema,
  loanTypeConfig,
  getCombinedSchema,
} from '../utils/loanSchemas';


const LoanApplicationPage = () => {
  const { loanType } = useParams(); // Get loanType from URL
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 3; // Customer Details, Loan Details, Summary

  // Initialize useForm with a dynamic resolver
  const methods = useForm({
    resolver: yupResolver(getCombinedSchema(currentStep, loanType)), // Resolver directly depends on currentStep and loanType
    defaultValues: {
      customerName: '',
      customerEmail: '',
      customerPhone: '',
      loanType: loanTypeConfig[loanType]?.title || loanType, // Store the friendly loan type name
      savingsBalance: '',
      loanAmountRequested: '',
      guaranteesDescription: '',
      monthlySalary: '',
      employerName: '',
      employmentStartDate: '',
      fixedIncomeSourceDescription: '',
      monthlyFixedIncomeAmount: '',
      existingFinancialObligations: '',
      propertyAddress: '',
      propertyMarketValue: '',
      propertyDescription: '',
    },
    mode: 'onBlur',
  });

  const { getValues, setValue, trigger, handleSubmit, formState: { errors } } = methods;

  // Set the loanType value in the form data as soon as component mounts or loanType changes
  useEffect(() => {
    setValue('loanType', loanTypeConfig[loanType]?.title || loanType);
  }, [loanType, setValue]);

  const handleNext = async () => {
    let fieldsToValidate = [];
    if (currentStep === 1) {
      fieldsToValidate = Object.keys(customerDetailsSchema.fields);
    } else if (currentStep === 2 && loanTypeConfig[loanType]) {
      fieldsToValidate = Object.keys(loanTypeConfig[loanType].schema.fields);
    }

    const isValid = await trigger(fieldsToValidate);

    if (isValid) {
      setCurrentStep((prevStep) => Math.min(prevStep + 1, totalSteps));
    } else {
        console.log("Validation errors:", errors);
    }
  };

  const handlePrevious = () => {
    setCurrentStep((prevStep) => Math.max(prevStep - 1, 1));
  };

  const onSubmit = (data) => {
    console.log('Final Loan Application Data:', data);
    alert(`Loan Application for ${data.loanType} Submitted! Check console for data.`);
    // Here you would typically send the 'data' to your backend
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return <CustomerDetailsForm />;
      case 2:
        const LoanSpecificFormComponent = loanTypeConfig[loanType]?.component;
        return LoanSpecificFormComponent ? React.createElement(LoanSpecificFormComponent) : (
          <div className="text-red-500 text-center">Invalid Loan Type Selected.</div>
        );
      case 3:
        return <SummaryForm loanType={loanType} />; // Pass loanType to SummaryForm
      default:
        return null;
    }
  };

  const currentStepsList = loanTypeConfig[loanType]?.steps || ['Step 1', 'Step 2', 'Step 3']; // Default if config not found

  if (!loanTypeConfig[loanType]) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-2xl text-center">
          <h2 className="text-2xl font-bold mb-4 text-red-600">Error: Loan Type Not Found</h2>
          <p className="text-gray-700">The loan type "{loanType}" is not recognized. Please go back to the dashboard and select a valid loan type.</p>
          <button
            onClick={() => window.history.back()}
            className="mt-6 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-2xl">
        <h1 className="text-center text-2xl font-semibold mb-8 text-gray-800">Apply for {loanTypeConfig[loanType]?.title || 'Loan'}</h1>

        {/* Step Indicator */}
        <StepIndicator currentStep={currentStep} steps={currentStepsList} />

        {/* FormProvider wraps the entire form structure */}
        <FormProvider {...methods}>
          <form onSubmit={handleSubmit(onSubmit)}>
            {/* Form Content */}
            <div className="form-content">
              {renderStepContent()}
            </div>

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8">
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={handlePrevious}
                  className="flex items-center text-green-600 hover:text-green-800 font-semibold py-2 px-4 rounded"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path></svg>
                  Previous
                </button>
              )}
              {currentStep < totalSteps ? (
                <button
                  type="button"
                  onClick={handleNext}
                  className={`ml-auto bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg ${currentStep === 1 ? 'ml-auto' : ''}`}
                >
                  Next
                  <svg className="inline-block w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path></svg>
                </button>
              ) : (
                <button
                  type="submit"
                  className="ml-auto bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg"
                >
                  Submit Application
                </button>
              )}
            </div>
          </form>
        </FormProvider>
      </div>
    </div>
  );
};

export default LoanApplicationPage;