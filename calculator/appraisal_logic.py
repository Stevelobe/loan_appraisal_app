import math
from decimal import Decimal, getcontext

# Set precision for Decimal calculations
getcontext().prec = 10

# --- Global Loan Policy Constants (Example Values - Adjust as per Union Policy) ---
MORTGAGE_LOAN_MAX_AMOUNT = Decimal('500000000')
MORTGAGE_LOAN_MAX_TENURE_YEARS = 10
SALARY_BACKED_LOAN_MAX_AMOUNT = Decimal('10000000') # 10M XAF per policy
SAVINGS_GE_1_10_LOAN_RATIO = Decimal('0.10') # 1/10 of loan requested
LOAN_DURATION_LE_1_YEAR_MONTHS = 12 # For Standing Order Loans
SAVINGS_BALANCE_GE_1_5_LOAN_RATIO = Decimal('0.20') # 1/5 of loan requested
AGRICULTURAL_LOAN_CROPS_MAX_MONTHS = 6 # 6 months for crops
AGRICULTURAL_LOAN_LIVESTOCK_MAX_MONTHS = 12 # 12 months for livestock
EXPRESS_LOAN_MAX_MONTHS = 3 # 3 months for express loan
EXPRESS_LOAN_SAVINGS_GE_1_10_LOAN_RATIO = Decimal('0.10') # 1/10 or 10% for express loan

# NEW CONSTANT for Business Loan
BUSINESS_LOAN_MAX_AMOUNT = Decimal('25000000') # Example: 25M XAF cap for business loans
BUSINESS_LOAN_MAX_TENURE_YEARS = 5 # Example: 5 years max tenure for business loans

# --- Scoring Thresholds (Common to all loan types) ---
APPROVAL_THRESHOLD = Decimal('70')
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

def calculate_dti_ratio(gross_monthly_income, total_monthly_debt):
    """
    Calculates the Debt-to-Income (DTI) ratio.
    DTI = (Total Monthly Debt Payments / Gross Monthly Income) * 100
    """
    if gross_monthly_income <= 0:
        return Decimal('inf') # Cannot calculate DTI if income is zero or negative
    dti = (total_monthly_debt / gross_monthly_income) * 100
    return dti.quantize(Decimal('0.01'))


def calculate_loan_to_income_ratio(loan_amount, annual_income):
    """
    Calculates the Loan Amount to Annual Income Ratio.
    """
    if annual_income <= 0:
        return Decimal('inf')
    ratio = loan_amount / annual_income
    return ratio.quantize(Decimal('0.01'))


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
        # For now, assuming 0 can be a valid answer for these specific fields.
        # If a non-zero value is strictly required, add a check like `and value == 0`
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

    land_title_document_present = data.get('land_title_document', False)
    power_of_attorney_document_present = data.get('power_of_attorney_document', False)

    # Check if legal_mortgage_agreement_document is provided (it's passed as a bool from views.py)
    legal_mortgage_agreement_document_provided = data.get('legal_mortgage_agreement_document', False)
    
    # Corrected: Now accepting supporting_documents as a boolean
    supporting_documents_present = data.get('supporting_documents', False)
    
    no_existing_npl = data.get('no_existing_npl', False)

    # 'loan_purpose_document' is the key used in views.py for loan_instance.loan_purpose (TextField)
    loan_purpose_text = data.get('loan_purpose_document', '') 

    # Calculate monthly payment for the new loan
    monthly_payment_new_loan = calculate_monthly_payment(
        loan_amount, annual_interest_rate, loan_term_years
    )
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)

    # --- Appraisal Criteria ---

    # 1. Collateral (Land Title OR Power of Attorney) - Combined Check
    if land_title_document_present or power_of_attorney_document_present:
        total_score += Decimal('25')
        reasons.append("✔ Primary Collateral (Land Title OR Power of Attorney) is provided. (+25%)")
    else:
        reasons.append("✖ Neither Land Title nor Power of Attorney provided for primary collateral. (+0%)")

    # 2. Legal Mortgage Agreement
    if legal_mortgage_agreement_document_provided:
        total_score += Decimal('30')
        reasons.append("✔ Legal Mortgage Agreement on Land Title provided. (+30%)")
    else:
        reasons.append("✖ Legal Mortgage Agreement on Land Title not provided. (+0%)")

    # 3. Purpose of Loan (Text Field) - Using the corrected field name 'loan_purpose_document'
    # This assumes loan_purpose_text is still a string
    if loan_purpose_text and len(loan_purpose_text.strip()) >= 20:
        total_score += Decimal('5')
        reasons.append("✔ Purpose of Loan clearly stated. (+5%)")
    else:
        reasons.append("ℹ️ Purpose of Loan not clearly stated or too short. (+0%)")

    # 4. Supporting Documents (BOOLEAN Field) - CORRECTED LOGIC
    if supporting_documents_present: # Simply check if the boolean is True
        total_score += Decimal('5')
        reasons.append("✔ Supporting documents confirmed as present. (+5%)")
    else:
        reasons.append("ℹ️ Supporting documents not confirmed as present. (+0%)")

    # 5. No Existing Non-Performing Loan (NPL)
    if no_existing_npl:
        total_score += Decimal('5')
        reasons.append("✔ No existing Non-Performing Loan (NPL) detected. (+5%)")
    else:
        reasons.append("✖ Existing Non-Performing Loan (NPL) detected. (+0%)")

    # 6. Full KYC (Character)
    if _check_full_kyc(data):
        total_score += Decimal('10')
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 7. Loan Amount Policy Check
    # Ensure MORTGAGE_LOAN_MAX_AMOUNT is defined (e.g., at the top of this file or imported)
    if loan_amount <= MORTGAGE_LOAN_MAX_AMOUNT:
        total_score += Decimal('5')
        reasons.append(f"✔ Loan Amount ({loan_amount:,.0f} XAF) is within Union Policy ({MORTGAGE_LOAN_MAX_AMOUNT:,.0f} XAF cap). (+5%)")
    else:
        reasons.append(f"✖ Loan Amount ({loan_amount:,.0f} XAF) exceeds Union Policy ({MORTGAGE_LOAN_MAX_AMOUNT:,.0f} XAF cap). (+0%)")

    # 8. Loan Term Policy Check
    # Ensure MORTGAGE_LOAN_MAX_TENURE_YEARS is defined
    if loan_term_years <= MORTGAGE_LOAN_MAX_TENURE_YEARS:
        total_score += Decimal('5')
        reasons.append(f"✔ Loan Duration ({loan_term_years} years) is within Union Policy ({MORTGAGE_LOAN_MAX_TENURE_YEARS} years max). (+5%)")
    else:
        reasons.append(f"✖ Loan Duration ({loan_term_years} years) exceeds Union Policy ({MORTGAGE_LOAN_MAX_TENURE_YEARS} years max). (+0%)")

    # 9. Debt-to-Income (DTI) Ratio (Capacity)
    dti_percentage = Decimal('0')
    if borrower_gross_monthly_income > Decimal('0'):
        dti_percentage = (total_monthly_debt / borrower_gross_monthly_income) * Decimal('100')

        if dti_percentage <= Decimal('40'):
            total_score += Decimal('10')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 40% of Gross Income ({borrower_gross_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+10%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 40% of Gross Income ({borrower_gross_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Gross Monthly Income is zero or negative. (+0%)")

    # 10. Loan Amount to Annual Income Ratio (Capacity)
    loan_amount_to_annual_income_ratio = Decimal('0')
    if annual_income > Decimal('0'):
        loan_amount_to_annual_income_ratio = (loan_amount / annual_income)

        if loan_amount_to_annual_income_ratio <= 3:
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤3x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>3x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

    # --- Approval Decision ---
    approved_status = None
    # Ensure APPROVAL_THRESHOLD and BOARD_REVIEW_THRESHOLD are defined
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    elif total_score >= BOARD_REVIEW_THRESHOLD:
        approved_status = None # Requires manual review
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
        'estimated_net_monthly_income': float(borrower_gross_monthly_income * Decimal('0.8')),
        'loan_amount_to_annual_income_ratio': float(loan_amount_to_annual_income_ratio),
    }

def appraise_business_loan(data):
    """
    Appraises a Business Loan application based on defined criteria.
    """
    total_score = Decimal('0')
    reasons = []

    # General loan parameters (from base LoanApplication)
    loan_amount = data.get('loan_amount')
    annual_interest_rate = data.get('annual_interest_rate_percent')
    loan_term_years = data.get('loan_term_years')
    borrower_gross_monthly_income = data.get('borrower_gross_monthly_income')
    existing_monthly_debt_payments = data.get('existing_monthly_debt_payments', Decimal('0'))
    
    # Business Loan specific fields
    valid_source_of_income_for_repayment = data.get('valid_source_of_income_for_repayment', False)
    savings_balance_ge_20_percent_loan = data.get('savings_balance_ge_20_percent_loan', False)
    cost_estimate_provided = data.get('cost_estimate_provided', False)
    land_documents_attached_provided = bool(data.get('land_documents_attached')) # Check if FileField has a value

    # Calculate monthly payment for the new loan
    monthly_payment_new_loan = calculate_monthly_payment(
        loan_amount, annual_interest_rate, loan_term_years
    )
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    dti_percentage = Decimal('0')
    if borrower_gross_monthly_income > Decimal('0'):
        dti_percentage = (total_monthly_debt / borrower_gross_monthly_income) * Decimal('100')
    
    # --- Appraisal Criteria for Business Loan ---

    # 1. Valid Source of Income for Repayment (30 points)
    if valid_source_of_income_for_repayment:
        total_score += Decimal('30')
        reasons.append("✔ Valid source of income for repayment provided. (+30%)")
    else:
        reasons.append("✖ Valid source of income for repayment is required. (+0%)")

    # 2. Savings Balance >= 20% of Loan (25 points)
    if savings_balance_ge_20_percent_loan:
        total_score += Decimal('25')
        reasons.append("✔ Savings balance is at least 20% of the loan amount. (+25%)")
    else:
        reasons.append("✖ Savings balance is less than 20% of the loan amount. (+0%)")

    # 3. Cost Estimate Provided (15 points)
    if cost_estimate_provided:
        total_score += Decimal('15')
        reasons.append("✔ Cost estimate of purchases provided. (+15%)")
    else:
        reasons.append("✖ Cost estimate of purchases not provided. (+0%)")

    # 4. Land Documents Attached (10 points)
    if land_documents_attached_provided:
        total_score += Decimal('10')
        reasons.append("✔ Copies of land documents attached. (+10%)")
    else:
        reasons.append("ℹ️ No land documents attached. (+0%)") # Can be info if not strictly required for all business loans

    # 5. Full KYC (Character) (10 points)
    if _check_full_kyc(data):
        total_score += Decimal('10')
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 6. Debt-to-Income (DTI) Ratio (Capacity) (10 points)
    if borrower_gross_monthly_income > Decimal('0') and dti_percentage <= Decimal('50'): # A slightly higher DTI might be acceptable for business loans
        total_score += Decimal('10')
        reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 50% of Gross Income ({borrower_gross_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+10%)")
    else:
        reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 50% of Gross Income ({borrower_gross_monthly_income:,.0f} XAF) or income is zero. DTI: {dti_percentage:.1f}%. (+0%)")

    # 7. Loan Amount Policy Check (implicitly part of overall score, but good to check explicitly)
    if loan_amount <= BUSINESS_LOAN_MAX_AMOUNT:
        reasons.append(f"✔ Loan Amount ({loan_amount:,.0f} XAF) is within Union Policy ({BUSINESS_LOAN_MAX_AMOUNT:,.0f} XAF cap).")
    else:
        reasons.append(f"✖ Loan Amount ({loan_amount:,.0f} XAF) exceeds Union Policy ({BUSINESS_LOAN_MAX_AMOUNT:,.0f} XAF cap).")
        # No score added/subtracted here, as it's a hard policy check, but important for reasons.

    # 8. Loan Term Policy Check
    if loan_term_years <= BUSINESS_LOAN_MAX_TENURE_YEARS:
        reasons.append(f"✔ Loan Duration ({loan_term_years} years) is within Union Policy ({BUSINESS_LOAN_MAX_TENURE_YEARS} years max).")
    else:
        reasons.append(f"✖ Loan Duration ({loan_term_years} years) exceeds Union Policy ({BUSINESS_LOAN_MAX_TENURE_YEARS} years max).")
        # No score added/subtracted here, as it's a hard policy check, but important for reasons.

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

    # --- Approval Decision ---
    approved_status = None
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    elif total_score >= BOARD_REVIEW_THRESHOLD:
        approved_status = None # Requires manual review
    else:
        approved_status = False

    return {
        'score': float(total_score),
        'approved': approved_status,
        'reasons': reasons,
        'monthly_payment_new_loan': float(monthly_payment_new_loan),
        'total_monthly_debt': float(total_monthly_debt),
        'dti_percentage': float(dti_percentage),
        'estimated_net_monthly_income': float(borrower_gross_monthly_income * Decimal('0.8')) # Assuming 80% is net
    }


def appraise_salary_backed_loan(data):
    """
    Appraises a Salary-Backed Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))

    salary_passing_union_ge_3_months = data.get('salary_passing_union_ge_3_months', False)
    savings_ge_1_10_loan = data.get('savings_ge_1_10_loan', False)
    copy_of_effective_service_document = data.get('copy_of_effective_service_document', False)
    irrevocable_salary_transfer_document = data.get('irrevocable_salary_transfer_document', False)
    loan_purpose_document_text = data.get('loan_purpose_document', '')

    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio # For consistency in return, though it's already a percentage from calculate_dti_ratio

    # --- Appraisal Criteria ---

    # 1. Document-based Criteria (Checks if file was provided or text is present)
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Defined"},
        'copy_of_effective_service_document': {'weight': 15, 'notes': "Copy of Effective Service"},
        'irrevocable_salary_transfer_document': {'weight': 20, 'notes': "Irrevocable Salary Transfer Document"},
    }
    for field, details in doc_criteria.items():
        if field == 'loan_purpose_document':
            if data.get(field) and len(data.get(field).strip()) > 0:
                total_score += Decimal(str(details['weight']))
                reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
            else:
                reasons.append(f"ℹ️ {details['notes']} (Not Provided/Empty, +0%)")
        elif data.get(field): # For FileFields (converted to boolean in views), check if True
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Provided, +0%)")

    # 2. KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('10') # Weight for Full KYC
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 3. System-Check Criteria (Boolean fields)
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

    # 4. Policy Check: Loan Amount <= 10M (15%)
    if loan_amount <= SALARY_BACKED_LOAN_MAX_AMOUNT:
        total_score += Decimal('15')
        reasons.append(f"✔ Loan Amount ({loan_amount:,.0f} XAF) is ≤ 10M XAF per Union Policy. (+15%)")
    else:
        reasons.append(f"✖ Loan Amount ({loan_amount:,.0f} XAF) exceeds 10M XAF per Union Policy. (+0%)")

    # 5. Capacity Checks (DTI and Loan-to-Income)
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8') # Assuming 80% is net after taxes/deductions

    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('45'): # Slightly more lenient DTI for salary-backed
            total_score += Decimal('5')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 45% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+5%)")
        else:
            reasons.append(f"ℹ️ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 45% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    if annual_income > Decimal('0'):
        if loan_amount_to_annual_income_ratio <= 1.5: # Salary-backed loans are typically smaller relative to income
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤1.5x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>1.5x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

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

def appraise_loan_within_savings(data):
    """
    Appraises a Loan Within Savings application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))
    
    savings_covers_loan_plus_interest = data.get('savings_covers_loan_plus_interest', False)
    loan_amount_blocked_in_savings = data.get('loan_amount_blocked_in_savings', False)
    no_active_default = data.get('no_active_default', False)
    loan_purpose_document_text = data.get('loan_purpose_document', '')

    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio # For consistency in return

    # --- Appraisal Criteria ---

    # 1. Document-based Criteria (Checks if text is present)
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Defined"},
    }
    for field, details in doc_criteria.items():
        if data.get(field) and len(data.get(field).strip()) > 0:
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"ℹ️ {details['notes']} (Not Provided/Empty, +0%)")

    # 2. KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('10') # Weight for Full KYC
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 3. System-Check Criteria (Boolean fields)
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

    # 4. Capacity Checks (DTI and Loan-to-Income)
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')

    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('50'): # More lenient DTI as it's savings-backed
            total_score += Decimal('5')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 50% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+5%)")
        else:
            reasons.append(f"ℹ️ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 50% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    if annual_income > Decimal('0'):
        if loan_amount_to_annual_income_ratio <= 2: # Less critical for this loan type
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤2x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>2x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

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

def appraise_daily_savings_loan(data):
    """
    Appraises a Daily Savings Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))
    
    daily_savings_active_ge_6_months = data.get('daily_savings_active_ge_6_months', False)
    signed_deduction_agreement_document = data.get('signed_deduction_agreement_document', False)
    valid_surety_bond_document = data.get('valid_surety_bond_document', False)
    positive_loan_repayment_history = data.get('positive_loan_repayment_history', False)
    savings_balance_ge_1_5_loan = data.get('savings_balance_ge_1_5_loan', False)
    loan_purpose_document_text = data.get('loan_purpose_document', '')


    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio # For consistency in return

    # --- Appraisal Criteria ---

    # 1. Document-based Criteria
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Defined"},
        'signed_deduction_agreement_document': {'weight': 15, 'notes': "Signed Deduction Agreement from Daily Savings"},
        'valid_surety_bond_document': {'weight': 20, 'notes': "Signed Surety Bond (Valid Surety)"},
    }
    for field, details in doc_criteria.items():
        if field == 'loan_purpose_document':
            if data.get(field) and len(data.get(field).strip()) > 0:
                total_score += Decimal(str(details['weight']))
                reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
            else:
                reasons.append(f"ℹ️ {details['notes']} (Not Provided/Empty, +0%)")
        elif data.get(field):
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"✖ {details['notes']} (Not Provided, +0%)")

    # 2. KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('10') # Weight for Full KYC
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 3. System-Check Criteria
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

    # 4. Capacity Checks (DTI and Loan-to-Income)
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')

    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('45'):
            total_score += Decimal('10')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 45% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+10%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 45% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    if annual_income > Decimal('0'):
        if loan_amount_to_annual_income_ratio <= 2.5:
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤2.5x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>2.5x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

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

def appraise_standing_order_loan(data):
    """
    Appraises a Standing Order Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))
    
    standing_order_active_ge_3_months = data.get('standing_order_active_ge_3_months', False)
    loan_duration_le_1_year = data.get('loan_duration_le_1_year', False)
    savings_balance_ge_1_5_loan = data.get('savings_balance_ge_1_5_loan', False)
    no_existing_default_or_delinquency = data.get('no_existing_default_or_delinquency', False)
    loan_purpose_document_text = data.get('loan_purpose_document', '')

    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio # For consistency in return

    # --- Appraisal Criteria ---

    # 1. Document-based Criteria
    doc_criteria = {
        'loan_purpose_document': {'weight': 5, 'notes': "Purpose of Loan Clearly Stated & Valid"},
    }
    for field, details in doc_criteria.items():
        if data.get(field) and len(data.get(field).strip()) > 0:
            total_score += Decimal(str(details['weight']))
            reasons.append(f"✔ {details['notes']} (Provided, +{details['weight']}%)")
        else:
            reasons.append(f"ℹ️ {details['notes']} (Not Provided/Empty, +0%)")

    # 2. KYC Fields
    if _check_full_kyc(data):
        total_score += Decimal('15') # Weight for Full KYC for Standing Order (adjusted from 10% in others)
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+15%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 3. System-Check Criteria
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

    # 4. Capacity Checks (DTI and Loan-to-Income)
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')

    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('40'):
            total_score += Decimal('10')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 40% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+10%)")
        elif dti_percentage <= Decimal('50'):
            total_score += Decimal('5')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 50% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+5%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 50% of Estimated Net Income ({estimated_net_monthly_income:,.0f} XAF). DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    if annual_income > Decimal('0'):
        if loan_amount_to_annual_income_ratio <= 1:
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤1x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>1x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

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

def appraise_real_estate_loan(data):
    """
    Appraises a Real Estate Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))

    # Specific Real Estate Loan Fields (booleans from forms/views)
    loan_duration_ge_10_years = data.get('loan_duration_ge_10_years', False)
    loan_amount_le_10_percent_paid_up_capital = data.get('loan_amount_le_10_percent_paid_up_capital', False)
    legal_mortgage_agreement_document_re = data.get('legal_mortgage_agreement_document_re', False) # File field becomes boolean
    land_title_in_borrowers_name = data.get('land_title_in_borrowers_name', False)
    valid_proof_of_source_of_income = data.get('valid_proof_of_source_of_income', False)
    loan_purpose_document_text = data.get('loan_purpose_document', '')

    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio

    # --- Appraisal Criteria ---

    # 1. Specific Real Estate Checks (Weights are examples, adjust as needed)
    if loan_duration_ge_10_years:
        total_score += Decimal('10')
        reasons.append("✔ Loan duration is greater than or equal to 10 years. (+10%)")
    else:
        reasons.append("✖ Loan duration is less than 10 years. (+0%)")

    if loan_amount_le_10_percent_paid_up_capital:
        total_score += Decimal('15')
        reasons.append("✔ Loan amount does not exceed 10% of paid-up capital. (+15%)")
    else:
        reasons.append("✖ Loan amount exceeds 10% of paid-up capital. (+0%)")

    if legal_mortgage_agreement_document_re:
        total_score += Decimal('20')
        reasons.append("✔ Legal Mortgage Agreement signed and provided. (+20%)")
    else:
        reasons.append("✖ Legal Mortgage Agreement not provided. (+0%)")

    if land_title_in_borrowers_name:
        total_score += Decimal('15')
        reasons.append("✔ Land Title is in Borrower's Name. (+15%)")
    else:
        reasons.append("✖ Land Title is not in Borrower's Name. (+0%)")

    if valid_proof_of_source_of_income:
        total_score += Decimal('10')
        reasons.append("✔ Valid Proof of Source of Income provided. (+10%)")
    else:
        reasons.append("✖ No Valid Proof of Source of Income provided. (+0%)")

    # 2. Common Criteria (from other loan types, adjust weights if necessary)
    # Loan Purpose
    if loan_purpose_document_text and len(loan_purpose_document_text.strip()) >= 20:
        total_score += Decimal('5')
        reasons.append("✔ Purpose of Loan clearly stated. (+5%)")
    else:
        reasons.append("ℹ️ Purpose of Loan not clearly stated or too short. (+0%)")

    # KYC
    if _check_full_kyc(data):
        total_score += Decimal('10')
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # DTI
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')
    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('40'):
            total_score += Decimal('10')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 40% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+10%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 40% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    # Loan to Annual Income Ratio
    if annual_income > Decimal('0'):
        if loan_amount_to_annual_income_ratio <= 4: # Real estate loans can be higher relative to income
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤4x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>4x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

    # Approval Status
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

def appraise_container_loan(data):
    """
    Appraises a Container Loan application.
    This version removes the manual board review step; loans are either approved or rejected.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))

    # Specific Container Loan Fields
    bill_of_lading_document = data.get('bill_of_lading_document', False) # Boolean from FileField
    custom_clearance_plan_document = data.get('custom_clearance_plan_document', False) # Boolean from FileField
    savings_balance_amount = data.get('savings_balance_amount', Decimal('0.00')) # Decimal field
    savings_balance_ge_1_5_loan = data.get('savings_balance_ge_1_5_loan', False) # Boolean checkbox
    valid_proof_of_source_of_income = data.get('valid_proof_of_source_of_income', False) # Boolean checkbox
    loan_purpose_document_text = data.get('loan_purpose_document', '')

    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio # Assuming dti_ratio is already a percentage or will be treated as such

    # --- Appraisal Criteria ---

    # 1. Specific Container Loan Checks (Weights are examples, adjust as needed)
    if bill_of_lading_document:
        total_score += Decimal('20')
        reasons.append("✔ Copy of Bill of Lading provided. (+20%)")
    else:
        reasons.append("✖ Copy of Bill of Lading not provided. (+0%)")

    if custom_clearance_plan_document:
        total_score += Decimal('15')
        reasons.append("✔ Custom Clearance Plan provided. (+15%)")
    else:
        reasons.append("✖ Custom Clearance Plan not provided. (+0%)")

    # The savings_balance_amount is for data collection. The scoring is on the checkbox.
    # Ensure SAVINGS_BALANCE_GE_1_5_LOAN_RATIO is defined (e.g., at the top of this file)
    if savings_balance_ge_1_5_loan:
        total_score += Decimal('20')
        reasons.append(f"✔ Savings balance is ≥ 1/5 ({SAVINGS_BALANCE_GE_1_5_LOAN_RATIO*100:.0f}%) of the loan amount ({loan_amount:,.0f} XAF). (+20%)")
    else:
        reasons.append(f"✖ Savings balance is < 1/5 ({SAVINGS_BALANCE_GE_1_5_LOAN_RATIO*100:.0f}%) of the loan amount ({loan_amount:,.0f} XAF). (+0%)")

    if valid_proof_of_source_of_income:
        total_score += Decimal('15')
        reasons.append("✔ Valid Proof of Source of Income provided. (+15%)")
    else:
        reasons.append("✖ No Valid Proof of Source of Income provided. (+0%)")

    # Add the note if loan is above 10,000,000 XAF
    if loan_amount > Decimal('10000000'):
        reasons.append("ℹ️ Note: Legal mortgage recommended for loans above 10,000,000 XAF.")

    # 2. Common Criteria (from other loan types, adjust weights if necessary)
    # Loan Purpose
    if loan_purpose_document_text and len(loan_purpose_document_text.strip()) >= 20:
        total_score += Decimal('5')
        reasons.append("✔ Purpose of Loan clearly stated. (+5%)")
    else:
        reasons.append("ℹ️ Purpose of Loan not clearly stated or too short. (+0%)")

    # KYC
    if _check_full_kyc(data):
        total_score += Decimal('10')
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+10%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # DTI
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')
    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('45'): # Slightly more lenient DTI for commercial loans
            total_score += Decimal('5')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 45% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+5%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 45% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    # Loan to Annual Income Ratio (Container loans might have different income relation)
    if annual_income > Decimal('0'):
        if loan_amount_to_annual_income_ratio <= 5: # Example: allowing higher ratio for business loans
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤5x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>5x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

    # --- Approval Status (REMOVED BOARD_REVIEW_THRESHOLD) ---
    approved_status = None
    # Ensure APPROVAL_THRESHOLD is defined (e.g., at the top of this file)
    if total_score >= APPROVAL_THRESHOLD:
        approved_status = True
    else:
        approved_status = False # If not approved, it's rejected. No middle ground.

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

def appraise_agricultural_loan(data):
    """
    Appraises an Agricultural Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))

    # Specific Agricultural Loan Fields
    is_land_personal_belonging = data.get('is_land_personal_belonging', False)
    has_authorization_of_usage = data.get('has_authorization_of_usage', False)
    loan_purpose_category = data.get('loan_purpose_category') # 'crops' or 'livestock'
    savings_balance_amount = data.get('savings_balance_amount', Decimal('0.00'))
    savings_balance_ge_1_5_loan = data.get('savings_balance_ge_1_5_loan', False)
    total_cost_estimate_document = data.get('total_cost_estimate_document', False) # File field becomes boolean
    valid_proof_of_source_of_income = data.get('valid_proof_of_source_of_income', False) # Assuming this is a common check
    loan_purpose_document_text = data.get('loan_purpose_document', '')

    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio

    # --- Appraisal Criteria ---

    # 1. Land Ownership and Authorization (25%)
    if is_land_personal_belonging:
        total_score += Decimal('25')
        reasons.append("✔ Land is a personal belonging of the loan applicant. (+25%)")
    elif not is_land_personal_belonging and has_authorization_of_usage:
        total_score += Decimal('15') # Less weight if not personal but authorized
        reasons.append("✔ Land is not personal, but authorization of usage is provided. (+15%)")
    else:
        reasons.append("✖ Land ownership/authorization not confirmed. (+0%)")

    # 2. Loan Duration based on Purpose (15%)
    loan_term_months = loan_term_years * 12
    if loan_purpose_category == 'crops':
        if loan_term_months <= AGRICULTURAL_LOAN_CROPS_MAX_MONTHS:
            total_score += Decimal('15')
            reasons.append(f"✔ Loan duration ({loan_term_months} months) is suitable for crops (≤ {AGRICULTURAL_LOAN_CROPS_MAX_MONTHS} months). (+15%)")
        else:
            reasons.append(f"✖ Loan duration ({loan_term_months} months) exceeds maximum for crops (> {AGRICULTURAL_LOAN_CROPS_MAX_MONTHS} months). (+0%)")
    elif loan_purpose_category == 'livestock':
        if loan_term_months <= AGRICULTURAL_LOAN_LIVESTOCK_MAX_MONTHS:
            total_score += Decimal('15')
            reasons.append(f"✔ Loan duration ({loan_term_months} months) is suitable for livestock (≤ {AGRICULTURAL_LOAN_LIVESTOCK_MAX_MONTHS} months). (+15%)")
        else:
            reasons.append(f"✖ Loan duration ({loan_term_months} months) exceeds maximum for livestock (> {AGRICULTURAL_LOAN_LIVESTOCK_MAX_MONTHS} months). (+0%)")
    else:
        reasons.append("ℹ️ Loan purpose category not specified, duration check skipped. (+0%)")

    # 3. Savings Balance (20%)
    required_savings = loan_amount * SAVINGS_BALANCE_GE_1_5_LOAN_RATIO
    if savings_balance_ge_1_5_loan: # Checkbox indicates system verification
        total_score += Decimal('20')
        reasons.append(f"✔ Savings balance is ≥ 1/5 ({SAVINGS_BALANCE_GE_1_5_LOAN_RATIO*100:.0f}%) of the loan amount ({loan_amount:,.0f} XAF). (+20%)")
    else:
        reasons.append(f"✖ Savings balance is < 1/5 ({SAVINGS_BALANCE_GE_1_5_LOAN_RATIO*100:.0f}%) of the loan amount ({loan_amount:,.0f} XAF). (+0%)")

    # 4. Total Cost Estimate Document (10%)
    if total_cost_estimate_document:
        total_score += Decimal('10')
        reasons.append("✔ Total Cost Estimate of Products and Inputs document provided. (+10%)")
    else:
        reasons.append("✖ Total Cost Estimate document not provided. (+0%)")

    # 5. Valid Proof of Source of Income (10%)
    if valid_proof_of_source_of_income:
        total_score += Decimal('10')
        reasons.append("✔ Valid Proof of Source of Income provided. (+10%)")
    else:
        reasons.append("✖ No Valid Proof of Source of Income provided. (+0%)")

    # 6. Loan Purpose (Text Field - 5%)
    if loan_purpose_document_text and len(loan_purpose_document_text.strip()) >= 20:
        total_score += Decimal('5')
        reasons.append("✔ Purpose of Loan clearly stated. (+5%)")
    else:
        reasons.append("ℹ️ Purpose of Loan not clearly stated or too short. (+0%)")

    # 7. KYC (Character - 5%)
    if _check_full_kyc(data):
        total_score += Decimal('5')
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+5%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 8. DTI (Capacity - 5%)
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')
    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('50'): # Agricultural loans might have slightly higher DTI tolerance
            total_score += Decimal('5')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 50% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+5%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 50% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    # 9. Loan to Annual Income Ratio (Capacity - 5%)
    if annual_income > Decimal('0'):
        if loan_amount_to_annual_income_ratio <= 4: # Allowing higher ratio for agricultural business loans
            total_score += Decimal('5')
            reasons.append(f"✔ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is within acceptable limits (≤4x). (+5%)")
        else:
            reasons.append(f"ℹ️ Loan amount to annual income ratio ({loan_amount_to_annual_income_ratio:.2f}x) is high (>4x). (+0%)")
    else:
        reasons.append("✖ Cannot calculate loan to income ratio: Annual Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

    # Approval Status
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

# --- NEW APPRAISAL FUNCTION FOR EXPRESS LOAN ---
def appraise_express_loan(data):
    """
    Appraises an Express Loan application.
    """
    total_score = Decimal('0')
    reasons = []

    loan_amount = Decimal(data.get('loan_amount', '0.00'))
    annual_interest_rate = Decimal(data.get('annual_interest_rate_percent', '0.00'))
    loan_term_years = int(data.get('loan_term_years', 1))
    borrower_gross_monthly_income = Decimal(data.get('borrower_gross_monthly_income', '0.00'))
    existing_monthly_debt_payments = Decimal(data.get('existing_monthly_debt_payments', Decimal('0')))

    # Specific Express Loan Fields
    salary_deducted_at_source_or_standing_order = data.get('salary_deducted_at_source_or_standing_order', False)
    effective_service_available = data.get('effective_service_available', False)
    clearly_valid_purpose_of_loan = data.get('clearly_valid_purpose_of_loan', False)
    savings_balance_amount = data.get('savings_balance_amount', Decimal('0.00'))
    savings_balance_ge_1_10_loan = data.get('savings_balance_ge_1_10_loan', False)
    no_existing_delinquent_loan = data.get('no_existing_delinquent_loan', False)
    loan_purpose_document_text = data.get('loan_purpose_document', '') # General purpose field

    # Calculate common financial metrics
    monthly_payment_new_loan = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    total_monthly_debt = existing_monthly_debt_payments + monthly_payment_new_loan
    annual_income = borrower_gross_monthly_income * 12
    dti_ratio = calculate_dti_ratio(borrower_gross_monthly_income, total_monthly_debt)
    loan_amount_to_annual_income_ratio = calculate_loan_to_income_ratio(loan_amount, annual_income)
    dti_percentage = dti_ratio

    # --- Appraisal Criteria ---

    # 1. Loan Duration (25%) - Must not exceed 3 months (0.25 years)
    loan_term_months = loan_term_years * 12
    if loan_term_months <= EXPRESS_LOAN_MAX_MONTHS:
        total_score += Decimal('25')
        reasons.append(f"✔ Loan duration ({loan_term_months} months) is within policy (≤ {EXPRESS_LOAN_MAX_MONTHS} months). (+25%)")
    else:
        reasons.append(f"✖ Loan duration ({loan_term_months} months) exceeds maximum for Express Loan (> {EXPRESS_LOAN_MAX_MONTHS} months). (+0%)")

    # 2. Salary Deduction at Source or Standing Order (20%)
    if salary_deducted_at_source_or_standing_order:
        total_score += Decimal('20')
        reasons.append("✔ Salary deducted at source or standing order available. (+20%)")
    else:
        reasons.append("✖ Salary deduction at source or standing order not confirmed. (+0%)")

    # 3. Effective Service Available (15%)
    if effective_service_available:
        total_score += Decimal('15')
        reasons.append("✔ Effective Service document available. (+15%)")
    else:
        reasons.append("✖ Effective Service document not available. (+0%)")

    # 4. Clearly/Valid Purpose of Loan (10%)
    if clearly_valid_purpose_of_loan:
        total_score += Decimal('10')
        reasons.append("✔ Clearly and valid purpose of loan confirmed. (+10%)")
    else:
        reasons.append("✖ Purpose of loan is not clear or valid. (+0%)")

    # 5. Savings Balance (10%) - 1/10 or 10% of loan amount
    required_savings_express = loan_amount * EXPRESS_LOAN_SAVINGS_GE_1_10_LOAN_RATIO
    if savings_balance_ge_1_10_loan: # Checkbox indicates system verification
        total_score += Decimal('10')
        reasons.append(f"✔ Savings balance is ≥ 1/10 ({EXPRESS_LOAN_SAVINGS_GE_1_10_LOAN_RATIO*100:.0f}%) of the loan amount ({loan_amount:,.0f} XAF). (+10%)")
    else:
        reasons.append(f"✖ Savings balance is < 1/10 ({EXPRESS_LOAN_SAVINGS_GE_1_10_LOAN_RATIO*100:.0f}%) of the loan amount ({loan_amount:,.0f} XAF). (+0%)")

    # 6. No Existing Delinquent Loan (10%)
    if no_existing_delinquent_loan:
        total_score += Decimal('10')
        reasons.append("✔ No existing delinquent loan. (+10%)")
    else:
        reasons.append("✖ Existing delinquent loan detected. (+0%)")

    # 7. KYC (Character - 5%) - Reduced weight for express loans as speed is key
    if _check_full_kyc(data):
        total_score += Decimal('5')
        reasons.append("✔ Full KYC (ID, Place of Birth, Address, etc.) Provided. (+5%)")
    else:
        reasons.append("✖ Full KYC (ID, Place of Birth, Address, etc.) Not Fully Provided. (+0%)")

    # 8. DTI (Capacity - 5%) - Express loans might have tighter DTI due to short term
    estimated_net_monthly_income = borrower_gross_monthly_income * Decimal('0.8')
    if estimated_net_monthly_income > Decimal('0'):
        if dti_percentage <= Decimal('35'): # Tighter DTI for short-term, high-turnover loans
            total_score += Decimal('5')
            reasons.append(f"✔ Monthly Repayment ({total_monthly_debt:,.0f} XAF) is ≤ 35% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+5%)")
        else:
            reasons.append(f"✖ Monthly Repayment ({total_monthly_debt:,.0f} XAF) exceeds 35% of Estimated Net Income. DTI: {dti_percentage:.1f}%. (+0%)")
    else:
        reasons.append("✖ Cannot calculate repayment affordability: Estimated Net Income is zero or negative. (+0%)")

    # --- Cap total_score at 100% ---
    total_score = min(total_score, Decimal('100'))

    # Approval Status
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
