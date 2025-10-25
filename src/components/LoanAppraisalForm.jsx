import React, { useState, useCallback } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {StepOne} from './StepOne'; // Step 1: Applicant & Loan Info
import StepTwo from './StepTwo'; // Step 2: KYC Details
import { stepThreeMortgageSchema, stepThreeSalarySchema, stepThreeSavingsSchema, stepThreeDailySchema,
  stepThreeStandingOrderSchema, stepThreeRealEstateSchema, stepThreeContainerSchema, stepThreeAgriculturalSchema,
  stepThreeExpressSchema, stepThreeBusinessSchema
 } from './stepThreeSchema';
import StepThreeMortgage from './loan_details/MortgageFields';
import StepThreeSalary from './loan_details/SalaryBackedFields';
import StepThreeDaily from './loan_details/DailySavingsFields';
import StepThreeStandingOrder from './loan_details/StandingOrderFields';
import StepThreeRealEstate from './loan_details/RealEstateFields';
import StepThreeContainer from './loan_details/ContainerFields';
import StepThreeAgricultural from './loan_details/AgriculturalFields';
import StepThreeExpress from './loan_details/ExpressFields';
import StepThreeBusiness from './loan_details/BusinessFields';
import StepFourConfirmation from './StepFourConfirmation';
// --- Utility: Get the display label from the loan type value ---
const getLoanLabel = (loanTypes, value) => {
  const loan = loanTypes.find(type => type.value === value);
  return loan ? loan.label : 'Unknown Loan Type';
};

// Step 1 Schema: Applicant & Loan Info (Used by ALL loan types)
const stepOneSchema = yup.object().shape({
  applicant_name: yup.string().required('Applicant Name is required.'),
  applicant_email: yup.string().email('Must be a valid email.').required('Applicant Email is required.'),
  loan_amount: yup.number().typeError('Loan Amount must be a number.').positive('Loan Amount must be positive.').required('Loan Amount is required.'),
  annual_interest_rate_percent: yup.number().typeError('Interest Rate must be a number.').min(0, 'Must be 0 or greater.').max(100, 'Must be 100 or less.').required('Interest Rate is required.'),
  loan_term_years: yup.number().typeError('Loan Term must be a number.').integer('Must be a whole number of years.').positive('Loan Term must be positive.').required('Loan Term is required.'),
  borrower_gross_monthly_income: yup.number().typeError('Income must be a number.').positive('Income must be positive.').required('Gross Monthly Income is required.'),
  existing_monthly_debt_payments: yup.number().typeError('Debt Payments must be a number.').min(0, 'Must be 0 or greater.').required('Existing Debt Payments are required.'),
  account_number: yup.string().required('Account Number is required.'),
  date_of_loan: yup.date().typeError('Invalid date format.').required('Date of Loan is required.'),
  loan_purpose: yup.string().required('Loan Purpose is required.'),
});

// Step 2 Schema: KYC Details (Used by ALL loan types)
const stepTwoSchema = yup.object().shape({
  identity_card_number: yup.string().required('ID Card Number is required.'),
  place_of_birth: yup.string().required('Place of Birth is required.'),
  date_of_birth: yup.date().typeError('Invalid date format.').required('Date of Birth is required.'),
  current_address: yup.string().required('Current Address is required.'),
  marital_status: yup.string().required('Marital Status is required.'),
  duration_with_mfi_years: yup.number().typeError('Duration must be a number.').min(0, 'Cannot be negative.').required('Duration is required.'),
  num_loans_other_mfi: yup.number().typeError('Number of loans must be a number.').integer('Must be a whole number.').min(0, 'Cannot be negative.').required('Number of loans is required.'),
  profession: yup.string().required('Profession is required.'),
  current_location: yup.string().required('Current Location is required.'),
});
const stepFourConfirmationSchema = yup.object().shape({});
// Combine schemas for all steps
const validationSchema = [stepOneSchema, stepTwoSchema, stepThreeMortgageSchema, stepThreeSalarySchema, stepThreeSavingsSchema,
  stepThreeDailySchema, stepThreeStandingOrderSchema, stepThreeRealEstateSchema, stepThreeAgriculturalSchema, 
  stepThreeExpressSchema, stepThreeBusinessSchema];
const getValidationSchema = (loanType) => {
    // Basic steps common to all loans
    const schemas = [stepOneSchema, stepTwoSchema]; 
    // Add type-specific step 3
    if (loanType === 'mortgage-loan') {
        schemas.push(stepThreeMortgageSchema);
    } else if (loanType === 'salary-loan') {
        schemas.push(stepThreeSalarySchema);
    }else if (loanType === 'loan-within-saving') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeSavingsSchema);
    }else if (loanType === 'daily-loan') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeDailySchema);
    }else if (loanType === 'standing-order-loan') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeStandingOrderSchema);
    }else if (loanType === 'real-estate-loan') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeRealEstateSchema);
    }else if (loanType === 'container-loan') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeContainerSchema);
    }else if (loanType === 'agricultural-loan') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeAgriculturalSchema);
    }else if (loanType === 'express-loan') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeExpressSchema);
    }else if (loanType === 'business-loan') { // <-- NEW LOGIC HERE
        schemas.push(stepThreeBusinessSchema);
    }
    // Add other loan type schemas here later...
    schemas.push(stepFourConfirmationSchema);
    return schemas;
};
// --- The Main Component ---
const LoanAppraisalForm = ({ selectedLoanType, loanTypes, onBackToSelection }) => {
  const [currentStep, setCurrentStep] = useState(0); // 0-indexed: Step 1 is index 0
  const [formData, setFormData] = useState({});
  const [isLoading, setIsLoading] = useState(false); // <-- NEW
  const [submissionError, setSubmissionError] = useState(null); // <-- NEW
  const [submissionSuccess, setSubmissionSuccess] = useState(null)
  const loanLabel = getLoanLabel(loanTypes, selectedLoanType);
  const currentValidationSchemas = getValidationSchema(selectedLoanType);
    const totalSteps = currentValidationSchemas.length; // Dynamic step count!

    // Initialize react-hook-form methods
    const methods = useForm({
        resolver: yupResolver(currentValidationSchemas[currentStep]), 
        defaultValues: { 
            ...formData, 
            selectedLoanType: selectedLoanType // <-- CRITICAL: Include loan type for Step 4
        }, 
        mode: 'onTouched', 
    });
    const { trigger, getValues, formState: { errors } } = methods;

  // Handler to move to the next step
  // Handler to move to the next step
  const handleNext = useCallback(async () => {
    // 1. Trigger validation for the current step's fields
    // NOTE: We trigger validation only for fields in the CURRENT step's schema
    const isStepValid = await trigger();

    if (isStepValid) {
      // 2. Save the current step's data (Crucial to persist data for Step 4 review)
      setFormData(prev => ({ ...prev, ...getValues() }));
      
      // 3. Move to the next step
      if (currentStep < totalSteps - 1) { 
        setCurrentStep(prev => prev + 1);
      } else {
        // If currentStep is the last index, submission happens via the button's 'submit' type.
        console.log("Ready for final submission on Step 4.");
      }
    } else {
        console.error("Validation Errors:", errors);
    }
  }, [currentStep, totalSteps, trigger, getValues, formData, errors]);

  // Handler to move to the previous step
  const handlePrev = useCallback(() => {
    // Save current step data before going back (in case user made changes)
    setFormData(prev => ({ ...prev, ...getValues() })); 
    setCurrentStep(prev => prev - 1);
  }, [getValues]);
 
  // Render the appropriate step component
  // Render the appropriate step component
  const renderStep = () => {
        const totalSteps = currentValidationSchemas.length; 

    // RENDER CONFIRMATION STEP: If we are at the last index
    if (currentStep === totalSteps - 1) {
        return <StepFourConfirmation />; // This is Step 4
    }

        // RENDER DATA ENTRY STEPS
        switch (currentStep) {
          case 0:
            return <StepOne />;
          case 1:
            return <StepTwo />;
          case 2: 
                // Step 3 (index 2) must be rendered if the loan has 3 or more steps (totalSteps > 2)
                if (totalSteps > 2) {
                    if(selectedLoanType === 'mortgage-loan') {
                        return <StepThreeMortgage/>
                    }else if (selectedLoanType === 'salary-loan') { 
                        return <StepThreeSalary />;
                    }else if (selectedLoanType === 'loan-within-saving') { 
                        return <StepThreeSavings />;
                    }else if (selectedLoanType === 'daily-loan') { 
                        return <StepThreeDaily />;
                    }else if (selectedLoanType === 'standing-order-loan') { 
                        return <StepThreeStandingOrder />;
                    }else if (selectedLoanType === 'real-estate-loan') { 
                        return <StepThreeRealEstate />;
                    }else if (selectedLoanType === 'container-loan') { 
                        return <StepThreeContainer />;
                    }else if (selectedLoanType === 'agricultural-loan') { 
                        return <StepThreeAgricultural />;
                    }else if (selectedLoanType === 'express-loan') { 
                        return <StepThreeExpress />;
                    }else if (selectedLoanType === 'business-loan') { 
                        return <StepThreeBusiness />;
                    }
                }
                // Fallthrough logic should not be reached if validation schemas are correct
                return <div>Error: Step 3 component missing or loan type has too few steps.</div>; 

          default:
            return <div>Error: Invalid Step Index ({currentStep})</div>;
        }
  };

  // Locate the handleSubmit function and replace the final submission logic:

const handleFinalSubmit = async (values) => {
  console.log('pop')
    // // Check if we are on the final confirmation step
    // if (currentStep < MAX_STEPS) {
    //     // This should not happen if the Next button logic is correct, but good for safety
    //     return; 
    // }

    // // --- Final API Submission Logic (Step 4) ---
    // setIsLoading(true);
    // setSubmissionError(null);

    // // 1. Prepare data for FormData (required for file uploads)
    // const formData = new FormData();
    // Object.entries(values).forEach(([key, value]) => {
    //     // Append all values, handling Files and Booleans correctly
    //     if (value instanceof File) {
    //         formData.append(key, value, value.name);
    //     } else if (typeof value === 'boolean') {
    //         formData.append(key, value ? 'true' : 'false');
    //     } else if (value !== null && value !== undefined) {
    //         formData.append(key, String(value));
    //     }
    // });

    // const API_ENDPOINT = "/api/loan-appraisal/submit"; // Replace with your actual endpoint

    // try {
    //     const response = await axios.post(API_ENDPOINT, formData, {
    //         headers: {
    //             // Ensure the content type is correctly set for file uploads
    //             'Content-Type': 'multipart/form-data'
    //         }
    //     });

    //     // 2. Handle Success
    //     setSubmissionSuccess({
    //         message: `Loan appraisal request for ${values.full_name} (${values.selected_loan_type}) submitted successfully!`,
    //         trackingId: response.data.tracking_id || 'N/A' // Assuming API returns a tracking ID
    //     });

    // } catch (error) {
    //     // 3. Handle Failure
    //     console.error("Submission error:", error.response || error);
    //     setSubmissionError(
    //         error.response?.data?.message || 
    //         "An unexpected error occurred during submission. Please check the network."
    //     );
    // } finally {
    //     setIsLoading(false);
    // }
};
const renderButtons = () => {
    const isLastStep = currentStep === totalSteps - 1;

    return (
      <div className="flex justify-between items-center pt-6 border-t border-slate-200">
        {/* Previous Button / Back to Selection */}
        {currentStep > 0 ? (
          <button
            type="button"
            onClick={handlePrev}
            disabled={isLoading}
            className="inline-flex items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition duration-150 disabled:opacity-50"
          >
            ⬅️ Previous
          </button>
        ) : (
          <button
            type="button"
            onClick={onBackToSelection}
            disabled={isLoading}
            className="inline-flex items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition duration-150 disabled:opacity-50"
          >
            🏠 Back to Loan Selection
          </button>
        )}

        {/* Next / Submit Button */}
        <button
          // If it's the last step, use type="submit" to trigger react-hook-form's final handler
          type={isLastStep ? 'submit' : 'button'} 
          onClick={isLastStep ? undefined : handleNext} // Only call handleNext for intermediate steps
          disabled={isLoading}
          className={`
            inline-flex items-center px-6 py-2 border border-transparent text-sm font-medium rounded-md shadow-lg text-white 
            ${isLastStep ? 'bg-green-600 hover:bg-green-700 focus:ring-green-500' : 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500'}
            focus:outline-none focus:ring-2 focus:ring-offset-2 transition duration-150 transform hover:scale-[1.02] disabled:opacity-50
          `}
        >
          {isLoading ? (
            <>⏳ Processing...</>
          ) : isLastStep ? (
            <>Submit Appraisal ✅</>
          ) : (
            <>Next Step ➡️</>
          )}
        </button>
      </div>
    );
  };
  // ... (rest of the component logic) ...

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-xl shadow-2xl border border-indigo-100">
      <div className="text-center pb-4 border-b border-indigo-300 mb-6">
        <h2 className="text-3xl font-extrabold text-indigo-700">
          Appraisal: {loanLabel}
        </h2>
        <p className="mt-2 text-lg text-slate-600">
          Step {currentStep + 1} of {totalSteps}: {currentStep === 0 ? 'Basic Information' : (currentStep === 1 ? 'Client Identity' : (currentStep === totalSteps - 1 ? 'Review & Submit' : 'Loan Specifics'))}
        </p>
      </div>

      {/* Progress Bar (Tailwind styling) */}
      <div className="mb-8">
        <div className="h-2 bg-slate-200 rounded-full">
          <div
            className="h-2 bg-indigo-500 rounded-full transition-all duration-500"
            style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
          ></div>
        </div>
      </div>
      
      {/* Submission Status Display (NEW) */}
      {submissionError && (
        <div className="p-4 mb-4 text-sm text-red-800 bg-red-100 rounded-lg" role="alert">
          <span className="font-medium">Error:</span> {submissionError}
        </div>
      )}
      {submissionSuccess && (
        <div className="p-4 mb-4 text-sm text-green-800 bg-green-100 rounded-lg" role="alert">
          <span className="font-medium">Success!</span> {submissionSuccess.message} (ID: {submissionSuccess.trackingId})
        </div>
      )}


      {/* Form Context Provider */}
      <FormProvider {...methods}>
        {/* IMPORTANT: Use methods.handleSubmit to trigger the final API function */}
        <form onSubmit={methods.handleSubmit(handleFinalSubmit)} className="space-y-6">
          {renderStep()}

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center pt-6 border-t border-slate-200">
                {/* Previous Button / Back to Selection */}
                {currentStep > 0 ? (
                    <button
                        type="button"
                        onClick={handlePrev}
                        disabled={isLoading}
                        className="inline-flex items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition duration-150 disabled:opacity-50"
                    >
                        ⬅️ Previous
                    </button>
                ) : (
                    <button
                        type="button"
                        onClick={onBackToSelection}
                        disabled={isLoading}
                        className="inline-flex items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition duration-150 disabled:opacity-50"
                    >
                        🏠 Back to Loan Selection
                    </button>
                )}

                {/* Next / Submit Button */}
                <button
                    // If it's the last step (totalSteps - 1), use type="submit"
                    type={currentStep === totalSteps - 1 ? 'submit' : 'button'} 
                    onClick={currentStep === totalSteps - 1 ? undefined : handleNext} 
                    disabled={isLoading}
                    className={`
                        inline-flex items-center px-6 py-2 border border-transparent text-sm font-medium rounded-md shadow-lg text-white 
                        ${currentStep === totalSteps - 1 ? 'bg-green-600 hover:bg-green-700 focus:ring-green-500' : 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500'}
                        focus:outline-none focus:ring-2 focus:ring-offset-2 transition duration-150 transform hover:scale-[1.02] disabled:opacity-50
                    `}
                >
                    {isLoading ? (
                        <>⏳ Processing...</>
                    ) : currentStep === totalSteps - 1 ? (
                        <>Submit Appraisal ✅</>
                    ) : (
                        <>Next Step ➡️</>
                    )}
                </button>
          </div>
        </form>
      </FormProvider>
    </div>
  );
};

export default LoanAppraisalForm;