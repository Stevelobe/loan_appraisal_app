import * as yup from 'yup';

// Step 3 Schema: Mortgage-Specific Details
export const stepThreeMortgageSchema = yup.object().shape({
    // File fields (can be handled as required strings for simplicity in yup)
    legal_mortgage_agreement_document: yup.mixed().required('A legal agreement document is required.'), 
    
    // Textarea field
    supporting_documents_notes: yup.string().nullable(),

    // Checkbox fields (boolean required)
    land_title_document_check: yup.boolean().oneOf([true], 'Land Title check must be confirmed.').required(),
    power_of_attorney_document_check: yup.boolean().oneOf([true], 'Power of Attorney check must be confirmed.').required(),
    no_existing_npl_check: yup.boolean().oneOf([true], 'NPL status must be confirmed.').required(),
});

// Step 3 Schema: Salary-Backed Specific Details
export const stepThreeSalarySchema = yup.object().shape({
    // File fields
    copy_of_effective_service_document: yup.mixed().required('The effective service document is required.'),
    irrevocable_salary_transfer_document: yup.mixed().required('The irrevocable salary transfer document is required.'),

    // Checkbox fields (boolean required)
    salary_passing_union_ge_3_months_check: yup.boolean().oneOf([true], 'Salary history must be confirmed.').required(),
    savings_ge_1_10_loan_check: yup.boolean().oneOf([true], 'Savings minimum must be confirmed.').required(),
});

// Step 3 Schema: Loan Within Savings Specific Details
export const stepThreeSavingsSchema = yup.object().shape({
    // Checkbox fields (boolean required)
    savings_covers_loan_plus_interest_check: yup.boolean().oneOf([true], 'Savings coverage must be confirmed.').required(),
    loan_amount_blocked_in_savings_check: yup.boolean().oneOf([true], 'Savings block must be confirmed.').required(),
    no_active_default_check: yup.boolean().oneOf([true], 'Active default status must be confirmed.').required(),
});

// Step 3 Schema: Daily Savings Loan Specific Details
export const stepThreeDailySchema = yup.object().shape({
    // File fields
    signed_deduction_agreement_document: yup.mixed().required('The deduction agreement is required.'),
    valid_surety_bond_document: yup.mixed().required('A valid surety bond document is required.'),

    // Checkbox fields (boolean required)
    daily_savings_active_ge_6_months_check: yup.boolean().oneOf([true], 'Daily Savings activity length must be confirmed.').required(),
    positive_loan_repayment_history_check: yup.boolean().oneOf([true], 'Repayment history must be confirmed.').required(),
    savings_balance_ge_1_5_loan_check: yup.boolean().oneOf([true], 'Minimum savings balance must be confirmed.').required(),
});

// Step 3 Schema: Standing Order Loan Specific Details
export const stepThreeStandingOrderSchema = yup.object().shape({
    // Checkbox fields (boolean required)
    standing_order_active_ge_3_months_check: yup.boolean().oneOf([true], 'Standing Order activity length must be confirmed.').required(),
    loan_duration_le_1_year_check: yup.boolean().oneOf([true], 'Loan duration limit must be confirmed.').required(),
    savings_balance_ge_1_5_loan_check: yup.boolean().oneOf([true], 'Minimum savings balance must be confirmed.').required(),
    no_existing_default_or_delinquency_check: yup.boolean().oneOf([true], 'Credit history must be confirmed.').required(),
});

// Step 3 Schema: Real Estate Loan Specific Details
export const stepThreeRealEstateSchema = yup.object().shape({
    // File field
    legal_mortgage_agreement_document_re: yup.mixed().required('The legal mortgage agreement document is required.'),

    // Checkbox fields (boolean required)
    loan_duration_ge_10_years_check: yup.boolean().oneOf([true], 'Loan duration check must be confirmed.').required(),
    loan_amount_le_10_percent_paid_up_capital_check: yup.boolean().oneOf([true], 'Paid-up capital limit check must be confirmed.').required(),
    land_title_in_borrowers_name_check: yup.boolean().oneOf([true], 'Land title ownership must be confirmed.').required(),
    valid_proof_of_source_of_income_check: yup.boolean().oneOf([true], 'Proof of income must be confirmed.').required(),
});

// Step 3 Schema: Container Loan Specific Details
export const stepThreeContainerSchema = yup.object().shape({
    // File fields
    bill_of_lading_document: yup.mixed().required('The Bill of Lading is required.'),
    custom_clearance_plan_document: yup.mixed().required('The Custom Clearance Plan is required.'),

    // Input field
    savings_balance_amount: yup.number()
        .typeError('Savings balance must be a number')
        .min(0, 'Savings balance cannot be negative.')
        .required('Savings balance amount is required for verification.'),

    // Checkbox fields (boolean required)
    savings_balance_ge_1_5_loan_check: yup.boolean().oneOf([true], 'Minimum savings balance ratio must be confirmed.').required(),
    valid_proof_of_source_of_income_check_container: yup.boolean().oneOf([true], 'Proof of income must be confirmed.').required(),
});

// Add this new schema after stepThreeContainerSchema

// Step 3 Schema: Agricultural Loan Specific Details
export const stepThreeAgriculturalSchema = yup.object().shape({
    // Checkbox fields (boolean required)
    is_land_personal_belonging_check: yup.boolean().oneOf([true], 'Land ownership status must be confirmed.').required(),
    has_authorization_of_usage_check: yup.boolean().oneOf([true], 'Land usage authorization must be confirmed.').required(),
    savings_balance_ge_1_5_loan_check_agri: yup.boolean().oneOf([true], 'Minimum savings balance ratio must be confirmed.').required(),
    valid_proof_of_source_of_income_check_agri: yup.boolean().oneOf([true], 'Proof of income must be confirmed.').required(),

    // Dropdown
    loan_purpose_category: yup.string().required('The loan purpose category must be selected.'),
    
    // Input field
    savings_balance_amount_agri: yup.number()
        .typeError('Savings balance must be a number')
        .min(0, 'Savings balance cannot be negative.')
        .required('Savings balance amount is required for verification.'),

    // File field
    total_cost_estimate_document: yup.mixed().required('The total cost estimate document is required.'),
});

// Add this new schema after stepThreeAgriculturalSchema

// Step 3 Schema: Express Loan Specific Details
export const stepThreeExpressSchema = yup.object().shape({
    // Input field
    savings_balance_amount_express: yup.number()
        .typeError('Savings balance must be a number')
        .min(0, 'Savings balance cannot be negative.')
        .required('Savings balance amount is required for verification.'),

    // Checkbox fields (boolean required)
    salary_deducted_at_source_or_standing_order_check: yup.boolean().oneOf([true], 'Repayment method must be confirmed.').required(),
    effective_service_available_check: yup.boolean().oneOf([true], 'Effective service status must be confirmed.').required(),
    clearly_valid_purpose_of_loan_check: yup.boolean().oneOf([true], 'Loan purpose must be confirmed.').required(),
    savings_balance_ge_1_10_loan_check: yup.boolean().oneOf([true], 'Minimum savings balance ratio must be confirmed.').required(),
    no_existing_delinquent_loan_check: yup.boolean().oneOf([true], 'Delinquency status must be confirmed.').required(),
});

// Add this new schema after stepThreeExpressSchema

// Step 3 Schema: Business Loan Specific Details
export const stepThreeBusinessSchema = yup.object().shape({
    // File fields
    business_registration_document: yup.mixed().required('The business registration document is required.'),
    financial_statements_document: yup.mixed().required('Financial statements for the last 3 years are required.'),
    business_plan_document: yup.mixed().required('A detailed business plan document is required.'),

    // Checkbox fields (boolean required)
    business_operational_min_3_years_check: yup.boolean().oneOf([true], 'Business operational history must be confirmed.').required(),
    adequate_collateral_assessed_check: yup.boolean().oneOf([true], 'Adequate collateral must be confirmed.').required(),
});