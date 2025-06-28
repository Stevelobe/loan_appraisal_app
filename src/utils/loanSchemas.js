// src/utils/loanSchemas.js

import * as yup from 'yup';

// Import loan-specific form components for use in loanTypeConfig
import SavingsLoanDetailsForm from '../components/forms/loanSpecific/SavingsLoanDetailsForm';
import AboveSavingsLoanDetailsForm from '../components/forms/loanSpecific/AboveSavingsLoanDetailsForm';
import SalaryLoanDetailsForm from '../components/forms/loanSpecific/SalaryLoanDetailsForm';
import StandingOrderLoanDetailsForm from '../components/forms/loanSpecific/StandingOrderLoanDetailsForm';
import MortgageLoanDetailsForm from '../components/forms/loanSpecific/MortgageLoanDetailsForm';


export const customerDetailsSchema = yup.object().shape({
  customerName: yup.string().required('Full Name is required'),
  customerEmail: yup.string().email('Invalid email format').required('Email is required'),
  customerPhone: yup.string().required('Phone Number is required').matches(/^(\d{9})$/, 'Invalid phone number format'),
});

export const savingsLoanDetailsSchema = yup.object().shape({
  savingsBalance: yup.number().typeError('Must be a number').positive('Must be positive').required('Savings Balance is required'),
  loanAmountRequested: yup.number().typeError('Must be a number').positive('Must be positive').required('Loan Amount is required')
    .max(yup.ref('savingsBalance'), 'Loan cannot exceed savings balance for this type'),
});

export const aboveSavingsLoanDetailsSchema = yup.object().shape({
  savingsBalance: yup.number().typeError('Must be a number').positive('Must be positive').required('Savings Balance is required'),
  loanAmountRequested: yup.number().typeError('Must be a number').positive('Must be positive').required('Loan Amount is required')
    .min(yup.ref('savingsBalance'), 'Loan must be greater than savings for this type'),
  guaranteesDescription: yup.string().required('Guarantees/Collateral description is required for loans above savings'),
});

export const salaryLoanDetailsSchema = yup.object().shape({
  monthlySalary: yup.number().typeError('Must be a number').positive('Must be positive').required('Monthly Salary is required'),
  loanAmountRequested: yup.number().typeError('Must be a number').positive('Must be positive').required('Loan Amount is required'),
  employerName: yup.string().required('Employer Name is required'),
  employmentStartDate: yup.date().typeError('Must be a valid date').required('Employment Start Date is required').max(new Date(), 'Start date cannot be in the future'),
});

export const standingOrderLoanDetailsSchema = yup.object().shape({
  fixedIncomeSourceDescription: yup.string().required('Fixed Income Source Description is required'),
  monthlyFixedIncomeAmount: yup.number().typeError('Must be a number').positive('Must be positive').required('Monthly Fixed Income Amount is required'),
  loanAmountRequested: yup.number().typeError('Must be a number').positive('Must be positive').required('Loan Amount is required'),
  existingFinancialObligations: yup.string().required('Existing Financial Obligations description is required'),
});

export const mortgageLoanDetailsSchema = yup.object().shape({
  propertyAddress: yup.string().required('Property Address is required'),
  propertyMarketValue: yup.number().typeError('Must be a number').positive('Must be positive').required('Property Market Value is required'),
  loanAmountRequested: yup.number().typeError('Must be a number').positive('Must be positive').required('Loan Amount is required')
    .max(yup.ref('propertyMarketValue'), 'Loan cannot exceed property market value'),
  propertyDescription: yup.string().required('Property Description is required'),
});

export const loanTypeConfig = {
  'savings-loan': {
    schema: savingsLoanDetailsSchema,
    component: SavingsLoanDetailsForm, // <--- ADD THIS LINE
    title: 'Loans within Savings',
    steps: ['Customer Details', 'Loan Details', 'Review & Submit'],
    relevantFields: [
      'customerName', 'customerEmail', 'customerPhone',
      'savingsBalance', 'loanAmountRequested',
    ],
  },
  'above-savings-loan': {
    schema: aboveSavingsLoanDetailsSchema,
    component: AboveSavingsLoanDetailsForm, // <--- ADD THIS LINE
    title: 'Loans Above Savings',
    steps: ['Customer Details', 'Loan Details', 'Review & Submit'],
    relevantFields: [
      'customerName', 'customerEmail', 'customerPhone',
      'savingsBalance', 'loanAmountRequested', 'guaranteesDescription',
    ],
  },
  'salary-loan': {
    schema: salaryLoanDetailsSchema,
    component: SalaryLoanDetailsForm, // <--- ADD THIS LINE
    title: 'Loans Covered by Salary',
    steps: ['Customer Details', 'Loan Details', 'Review & Submit'],
    relevantFields: [
      'customerName', 'customerEmail', 'customerPhone',
      'monthlySalary', 'loanAmountRequested', 'employerName', 'employmentStartDate',
    ],
  },
  'standing-order-loan': {
    schema: standingOrderLoanDetailsSchema,
    component: StandingOrderLoanDetailsForm, // <--- ADD THIS LINE
    title: 'Loans Covered by Standing Order',
    steps: ['Customer Details', 'Loan Details', 'Review & Submit'],
    relevantFields: [
      'customerName', 'customerEmail', 'customerPhone',
      'fixedIncomeSourceDescription', 'monthlyFixedIncomeAmount', 'loanAmountRequested', 'existingFinancialObligations',
    ],
  },
  'mortgage-loan': {
    schema: mortgageLoanDetailsSchema,
    component: MortgageLoanDetailsForm, // <--- ADD THIS LINE
    title: 'Mortgage Loans',
    steps: ['Customer Details', 'Loan Details', 'Review & Submit'],
    relevantFields: [
      'customerName', 'customerEmail', 'customerPhone',
      'propertyAddress', 'propertyMarketValue', 'loanAmountRequested', 'propertyDescription',
    ],
  },
};

export const getCombinedSchema = (currentStep, loanType) => {
  if (currentStep === 1) {
    return customerDetailsSchema;
  }
  if (currentStep === 2 && loanTypeConfig[loanType]) {
    return loanTypeConfig[loanType].schema;
  }
  return yup.object().shape({});
};