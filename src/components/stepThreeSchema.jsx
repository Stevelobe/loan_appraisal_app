import * as yup from 'yup';

// Step 3 Schema: Mortgage-Specific Details
export const stepThreeMortgageSchema = yup.object().shape({
    // File fields (can be handled as required strings for simplicity in yup)
    legal_mortgage_agreement_document: yup.boolean().default(false),
    
    // Textarea field
    supporting_documents_notes: yup.string().nullable(),

    // Checkbox fields (boolean required)
    land_title_document_check: yup.boolean().default(false),
    power_of_attorney_document_check: yup.boolean().default(false),
    no_existing_npl_check: yup.boolean().default(false),
});

// Step 3 Schema: Salary-Backed Specific Details
export const stepThreeSalarySchema = yup.object().shape({
    // File fields
    copy_of_effective_service_document: yup.boolean().default(false),
    irrevocable_salary_transfer_document: yup.boolean().default(false),

    // Checkbox fields (boolean required)
    salary_passing_union_ge_3_months_check: yup.boolean().default(false),
    savings_ge_1_10_loan_check: yup.boolean().default(false),
});

// Step 3 Schema: Loan Within Savings Specific Details
export const stepThreeSavingsSchema = yup.object().shape({
    // Checkbox fields (boolean required)
    savings_covers_loan_plus_interest_check: yup.boolean().default(false),
    loan_amount_blocked_in_savings_check: yup.boolean().default(false),
    no_active_default_check: yup.boolean().default(false),
});

// Step 3 Schema: Daily Savings Loan Specific Details
export const stepThreeDailySchema = yup.object().shape({
    // File fields
    signed_deduction_agreement_document: yup.boolean().default(false),
    valid_surety_bond_document: yup.boolean().default(false),

    // Checkbox fields (boolean required)
    daily_savings_active_ge_6_months_check: yup.boolean().default(false),
    positive_loan_repayment_history_check: yup.boolean().default(false),
    savings_balance_ge_1_5_loan_check: yup.boolean().default(false),
});

// Step 3 Schema: Standing Order Loan Specific Details
export const stepThreeStandingOrderSchema = yup.object().shape({
    // Checkbox fields (boolean required)
    standing_order_active_ge_3_months_check: yup.boolean().default(false),
    loan_duration_le_1_year_check: yup.boolean().default(false),
    savings_balance_ge_1_5_loan_check: yup.boolean().default(false),
    no_existing_default_or_delinquency_check: yup.boolean().default(false),
});

// Step 3 Schema: Real Estate Loan Specific Details
export const stepThreeRealEstateSchema = yup.object().shape({
    // File field
    legal_mortgage_agreement_document_re: yup.boolean().default(false),
    // Checkbox fields (boolean required)
    loan_duration_ge_10_years_check: yup.boolean().default(false),
    loan_amount_le_10_percent_paid_up_capital_check: yup.boolean().default(false),
    land_title_in_borrowers_name_check: yup.boolean().default(false),
    valid_proof_of_source_of_income_check: yup.boolean().default(false),
});

// Step 3 Schema: Container Loan Specific Details
export const stepThreeContainerSchema = yup.object().shape({
    // File fields
    bill_of_lading_document: yup.boolean().default(false),
    custom_clearance_plan_document: yup.boolean().default(false),

    // Input field
    savings_balance_amount: yup.number()
        .typeError('Savings balance must be a number')
        .min(0, 'Savings balance cannot be negative.')
        .required('Savings balance amount is required for verification.'),

    // Checkbox fields (boolean required)
    savings_balance_ge_1_5_loan_check: yup.boolean().default(false),
    valid_proof_of_source_of_income_check_container: yup.boolean().default(false),
});

// Add this new schema after stepThreeContainerSchema

// Step 3 Schema: Agricultural Loan Specific Details
export const stepThreeAgriculturalSchema = yup.object().shape({
    // Checkbox fields (boolean required)
    is_land_personal_belonging_check: yup.boolean().default(false),
    has_authorization_of_usage_check: yup.boolean().default(false),
    savings_balance_ge_1_5_loan_check_agri: yup.boolean().default(false),
    valid_proof_of_source_of_income_check_agri: yup.boolean().default(false),

    // Dropdown
    loan_purpose_category: yup.string().required('The loan purpose category must be selected.'),
    
    // Input field
    savings_balance_amount_agri: yup.number()
        .typeError('Savings balance must be a number')
        .min(0, 'Savings balance cannot be negative.')
        .required('Savings balance amount is required for verification.'),

    // File field
    total_cost_estimate_document: yup.boolean().default(false),
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
    salary_deducted_at_source_or_standing_order_check: yup.boolean().default(false),
    effective_service_available_check: yup.boolean().default(false),
    clearly_valid_purpose_of_loan_check: yup.boolean().default(false),
    savings_balance_ge_1_10_loan_check: yup.boolean().default(false),
    no_existing_delinquent_loan_check: yup.boolean().default(false),
});

// Add this new schema after stepThreeExpressSchema

// Step 3 Schema: Business Loan Specific Details
export const stepThreeBusinessSchema = yup.object().shape({
    // File fields
    business_registration_document: yup.boolean().default(false),
    financial_statements_document: yup.boolean().default(false),
    business_plan_document: yup.boolean().default(false),

    // Checkbox fields (boolean required)
    business_operational_min_3_years_check: yup.boolean().default(false),
    adequate_collateral_assessed_check: yup.boolean().default(false),
});