# calculator/appraisal_logic.py

import math
from decimal import Decimal

# --- Global Loan Policy Constants (Example Values - Adjust as per Union Policy) ---
MORTGAGE_LOAN_MAX_AMOUNT = Decimal('500000000')
MORTGAGE_LOAN_MAX_TENURE_YEARS = 10
SALARY_BACKED_LOAN_MAX_AMOUNT = Decimal('10000000') # 10M XAF per policy
SAVINGS_GE_1_10_LOAN_RATIO = Decimal('0.10') # 1/10 of loan requested
LOAN_DURATION_LE_1_YEAR_MONTHS = 12 # For Standing Order Loans
SAVINGS_BALANCE_GE_1_5_LOAN_RATIO = Decimal('0.20') # 1/5 of loan requested

# --- Scoring Thresholds (Common to all loan types) ---
APPROVAL_THRESHOLD = 96
BOARD_REVIEW_THRESHOLD = 75

def calculate_monthly_payment(principal, annual_interest_rate, loan_term_years):
    """
    Calculates the monthly loan payment using the annuity formula.
    Ensures all calculations are done with Decimal for precision.
    """
    if annual_interest_rate == Decimal('0'):
        # Simple interest for 0% rate
        return principal / (Decimal(loan_term_years) * Decimal('12'))

    monthly_interest_rate = (annual_interest_rate / Decimal('100')) / Decimal('12')
    number_of_payments = Decimal(loan_term_years) * Decimal('12')

    if number_of_payments == 0:
        return Decimal('0')

    try:
        term_raised_to_power = (Decimal('1') + monthly_interest_rate)**number_of_payments
        monthly_payment = principal * (monthly_interest_rate * term_raised_to_power) / \
                          (term_raised_to_power - Decimal('1'))
        return monthly_payment
    except ZeroDivisionError:
        return principal / (Decimal(loan_term_years) * Decimal('12'))

def _check_full_kyc(data):
    """
    Helper function to check if all new KYC fields are provided.
    """
    kyc_fields = [
        'identity_card_number', 'place_of_birth', 'current_address',
        'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi',
        'profession'
    ]
    # Check if all KYC fields are present and not empty/None
    for field in kyc_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            return False
        # For integer fields, ensure they are not 0 if that implies missing data
        if isinstance(value, int) and value == 0 and field in ['duration_with_mfi_years', 'num_loans_other_mfi']:
             # This is a judgment call: if 0 is a valid answer, remove this check.
             # For now, assuming 0 might mean "not provided" for these specific fields.
             pass # Let's allow 0 for now as it could be valid.
    return True

def appraise_mortgage_loan(data):
    """
    Appraises a Mortgage Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = data.get('loan_amount')
    annual_interest_rate = data.get('annual_interest_rate_percent')
    loan_term_years = data.get('loan_term_years')
    borrower_gross_monthly_income = data.get('borrower_gross_monthly_income')
    existing_monthly_debt_payments = data.get('existing_monthly_debt_payments', Decimal('0'))

    # --- Document-based Criteria (Checks if file was provided) ---
    doc_criteria = {
        'legal_mortgage_agreement_document': {'weight': 30, 'notes': "Legal Mortgage Agreement on Land Title"},
        'land_title_document': {'weight': 15, 'notes': "Land Title in Borrower's Name"},
        'power_of_attorney_document': {'weight': 10, 'notes': "Power of Attorney (if applicable)"},
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Stated & Valid (Document)"},
        'supporting_documents': {'weight': 5, 'notes': "Supporting Documents Uploaded (Site Plan, Quotes, etc.)"},
    }

    for field, details in doc_criteria.items():
        if data.get(field): # Check if file was provided
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Provided, +0%)")

    # --- KYC Fields (Replaces old full_kyc_document) ---
    if _check_full_kyc(data):
        total_score += Decimal('10') # Weight for Full KYC
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # --- System-Check Criteria (Boolean fields) ---
    sys_check_criteria = {
        'no_existing_npl': {'weight': 5, 'notes': "No Existing Non-Performing Loan (System Check)"},
    }
    for field, details in sys_check_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Met, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Met, +0%)")

    # --- Calculated/Policy-Based Criteria (remain unchanged) ---
    if loan_amount <= MORTGAGE_LOAN_MAX_AMOUNT:
        total_score += Decimal('5')
        reasons.append(f"✔ Loan Amount ({loan_amount:,.0f} XAF) is within Union Policy ({MORTGAGE_LOAN_MAX_AMOUNT:,.0f} XAF cap). (+5%)")
    else:
        reasons.append(f"✖ Loan Amount ({loan_amount:,.0f} XAF) exceeds Union Policy ({MORTGAGE_LOAN_MAX_AMOUNT:,.0f} XAF cap). (+0%)")

    if loan_term_years <= MORTGAGE_LOAN_MAX_TENURE_YEARS:
        total_score += Decimal('5')
        reasons.append(f"✔ Loan Duration ({loan_term_years} years) is within Union Policy ({MORTGAGE_LOAN_MAX_TENURE_YEARS} years max). (+5%)")
    else:
        reasons.append(f"✖ Loan Duration ({loan_term_years} years) exceeds Union Policy ({MORTGAGE_LOAN_MAX_TENURE_YEARS} years max). (+0%)")

    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = monthly_payment_new_loan + existing_monthly_debt_payments
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')

    dti_ratio = Decimal('0')
    dti_percentage = Decimal('0')

    if estimated_net_monthly_income > Decimal('0'):
        dti_ratio = (total_monthly_debt / estimated_net_monthly_income)
        dti_percentage = dti_ratio * Decimal('100')

        if dti_percentage <= Decimal('40'):
            total_score += Decimal('10')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 40% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+10%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 40% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero. (+0%)")

    loan_amount_to_annual_income_ratio = (loan_amount / (borrower_gross_monthly_income * Decimal('12'))) if borrower_gross_monthly_income > Decimal('0') else Decimal('0')

    approved_status = None
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    elif total_score >= BOARD_REVIEW_THRESHOLD:
        approved_status = None
    else:
        approved_status = False

    return {
        'score': float(total_score),
        'approved': approved_status,
        'reasons': reasons,
        'monthly_payment_new_loan': float(monthly_payment_new_loan),
        'total_monthly_debt': float(total_monthly_debt),
        'dti_ratio': float(dti_ratio),
        'dti_percentage': float(dti_percentage),
        'estimated_net_monthly_income': float(estimated_net_monthly_income),
        'loan_amount_to_annual_income_ratio': float(loan_amount_to_annual_income_ratio),
    }

def appraise_salary_backed_loan(data):
    """
    Appraises a Salary-Backed Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = data.get('loan_amount')
    dummy_monthly_payment = Decimal('0')
    dummy_total_monthly_debt = Decimal('0')
    dummy_dti_ratio = Decimal('0')
    dummy_dti_percentage = Decimal('0')
    dummy_estimated_net_monthly_income = Decimal('0')
    dummy_loan_amount_to_annual_income_ratio = Decimal('0')

    # Document-based Criteria
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Defined (Document)"},
        'copy_of_effective_service_document': {'weight': 15, 'notes': "Copy of Effective Service"},
        'irrevocable_salary_transfer_document': {'weight': 20, 'notes': "Irrevocable Salary Transfer Document"},
    }
    for field, details in doc_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Provided, +0%)")

    # KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('10') # Weight for Full KYC
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # System-Check Criteria
    sys_check_criteria = {
        'salary_passing_union_ge_3_months': {'weight': 20, 'notes': "Salary Passing Through Union for ≥ 3 Months"},
        'savings_ge_1_10_loan': {'weight': 15, 'notes': f"Savings ≥ {SAVINGS_GE_1_10_LOAN_RATIO*100:.0f}% of Loan Requested"},
    }
    for field, details in sys_check_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Met, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Met, +0%)")

    # Policy Check: Loan Amount <= 10M (15%)
    if loan_amount <= SALARY_BACKED_LOAN_MAX_AMOUNT:
        total_score += Decimal('15')
        reasons.append(f"✔ Loan Amount ({loan_amount:,.0f} XAF) is ≤ 10M XAF per Union Policy. (+15%)")
    else:
        reasons.append(f"✖ Loan Amount ({loan_amount:,.0f} XAF) exceeds 10M XAF per Union Policy. (+0%)")

    approved_status = None
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    elif total_score >= BOARD_REVIEW_THRESHOLD:
        approved_status = None
    else:
        approved_status = False

    return {
        'score': float(total_score),
        'approved': approved_status,
        'reasons': reasons,
        'monthly_payment_new_loan': float(dummy_monthly_payment),
        'total_monthly_debt': float(dummy_total_monthly_debt),
        'dti_ratio': float(dummy_dti_ratio),
        'dti_percentage': float(dummy_dti_percentage),
        'estimated_net_monthly_income': float(dummy_estimated_net_monthly_income),
        'loan_amount_to_annual_income_ratio': float(dummy_loan_amount_to_annual_income_ratio),
    }

def appraise_loan_within_savings(data):
    """
    Appraises a Loan Within Savings application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = data.get('loan_amount')
    dummy_monthly_payment = Decimal('0')
    dummy_total_monthly_debt = Decimal('0')
    dummy_dti_ratio = Decimal('0')
    dummy_dti_percentage = Decimal('0')
    dummy_estimated_net_monthly_income = Decimal('0')
    dummy_loan_amount_to_annual_income_ratio = Decimal('0')

    # Document-based Criteria
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Defined (Document)"},
    }
    for field, details in doc_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Provided, +0%)")

    # KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('10') # Weight for Full KYC
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # System-Check Criteria
    sys_check_criteria = {
        'savings_covers_loan_plus_interest': {'weight': 45, 'notes': "Savings Covers Loan + Interest for Entire Tenure"},
        'loan_amount_blocked_in_savings': {'weight': 35, 'notes': "Loan Amount Is Blocked in Savings Account"},
        'no_active_default': {'weight': 5, 'notes': "No Active Default/Delinquent Loan"},
    }
    for field, details in sys_check_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Met, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Met, +0%)")

    approved_status = None
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    elif total_score >= BOARD_REVIEW_THRESHOLD:
        approved_status = None
    else:
        approved_status = False

    return {
        'score': float(total_score),
        'approved': approved_status,
        'reasons': reasons,
        'monthly_payment_new_loan': float(dummy_monthly_payment),
        'total_monthly_debt': float(dummy_total_monthly_debt),
        'dti_ratio': float(dummy_dti_ratio),
        'dti_percentage': float(dummy_dti_percentage),
        'estimated_net_monthly_income': float(dummy_estimated_net_monthly_income),
        'loan_amount_to_annual_income_ratio': float(dummy_loan_amount_to_annual_income_ratio),
    }

def appraise_loan_above_savings(data):
    """
    Appraises a Loan Above Savings application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = data.get('loan_amount')
    dummy_monthly_payment = Decimal('0')
    dummy_total_monthly_debt = Decimal('0')
    dummy_dti_ratio = Decimal('0')
    dummy_dti_percentage = Decimal('0')
    dummy_estimated_net_monthly_income = Decimal('0')
    dummy_loan_amount_to_annual_income_ratio = Decimal('0')

    # Document-based Criteria
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Defined (Document)"},
        'signed_deduction_agreement_document': {'weight': 15, 'notes': "Signed Deduction Agreement from Daily Savings"},
        'valid_surety_bond_document': {'weight': 20, 'notes': "Signed Surety Bond (Valid Surety)"},
    }
    for field, details in doc_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Provided, +0%)")

    # KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('10') # Weight for Full KYC
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # System-Check Criteria
    sys_check_criteria = {
        'daily_savings_active_ge_6_months': {'weight': 20, 'notes': "Daily Savings Active for at Least 6 Months"},
        'positive_loan_repayment_history': {'weight': 15, 'notes': "Positive Loan Repayment History"},
        'savings_balance_ge_1_5_loan': {'weight': 15, 'notes': f"Savings Balance ≥ {SAVINGS_BALANCE_GE_1_5_LOAN_RATIO*100:.0f}% of Loan Requested"},
    }
    for field, details in sys_check_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Met, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Met, +0%)")

    approved_status = None
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    elif total_score >= BOARD_REVIEW_THRESHOLD:
        approved_status = None
    else:
        approved_status = False

    return {
        'score': float(total_score),
        'approved': approved_status,
        'reasons': reasons,
        'monthly_payment_new_loan': float(dummy_monthly_payment),
        'total_monthly_debt': float(dummy_total_monthly_debt),
        'dti_ratio': float(dummy_dti_ratio),
        'dti_percentage': float(dummy_dti_percentage),
        'estimated_net_monthly_income': float(dummy_estimated_net_monthly_income),
        'loan_amount_to_annual_income_ratio': float(dummy_loan_amount_to_annual_income_ratio),
    }

def appraise_standing_order_loan(data):
    """
    Appraises a Standing Order Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = data.get('loan_amount')
    loan_term_years = data.get('loan_term_years')

    dummy_monthly_payment = Decimal('0')
    dummy_total_monthly_debt = Decimal('0')
    dummy_dti_ratio = Decimal('0')
    dummy_dti_percentage = Decimal('0')
    dummy_estimated_net_monthly_income = Decimal('0')
    dummy_loan_amount_to_annual_income_ratio = Decimal('0')

    # Document-based Criteria
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Stated & Valid (Document)"},
    }
    for field, details in doc_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Provided, +0%)")

    # KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('15') # Weight for Full KYC for Standing Order (adjusted from 10% in others)
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+15%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # System-Check Criteria
    sys_check_criteria = {
        'standing_order_active_ge_3_months': {'weight': 30, 'notes': "Standing Order Active for ≥ 3 Months"},
        'loan_duration_le_1_year': {'weight': 20, 'notes': "Loan Duration ≤ 1 Year (Policy Restriction)"},
        'savings_balance_ge_1_5_loan': {'weight': 20, 'notes': f"Savings Balance ≥ {SAVINGS_BALANCE_GE_1_5_LOAN_RATIO*100:.0f}% of Loan Amount"},
        'no_existing_default_or_delinquency': {'weight': 10, 'notes': "No Existing Default or Delinquency"},
    }
    for field, details in sys_check_criteria.items():
        if data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Met, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Met, +0%)")

    approved_status = None
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    elif total_score >= BOARD_REVIEW_THRESHOLD:
        approved_status = None
    else:
        approved_status = False

    return {
        'score': float(total_score),
        'approved': approved_status,
        'reasons': reasons,
        'monthly_payment_new_loan': float(dummy_monthly_payment),
        'total_monthly_debt': float(dummy_total_monthly_debt),
        'dti_ratio': float(dummy_dti_ratio),
        'dti_percentage': float(dummy_dti_percentage),
        'estimated_net_monthly_income': float(dummy_estimated_net_monthly_income),
        'loan_amount_to_annual_income_ratio': float(dummy_loan_amount_to_annual_income_ratio),
    }