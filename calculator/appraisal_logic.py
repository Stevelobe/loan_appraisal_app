# calculator/appraisal_logic.py
import math

def calculate_monthly_payment(principal, annual_interest_rate, loan_term_months):
    """
    Calculates the monthly loan payment using the amortized loan formula.
    """
    if loan_term_months <= 0:
        return 0.0

    monthly_interest_rate = annual_interest_rate / 12

    if monthly_interest_rate == 0:
        return principal / loan_term_months
    else:
        numerator = monthly_interest_rate * (1 + monthly_interest_rate)**loan_term_months
        denominator = (1 + monthly_interest_rate)**loan_term_months - 1
        monthly_payment = principal * (numerator / denominator)
        return monthly_payment

def calculate_debt_to_income_ratio(gross_monthly_income, total_monthly_debt):
    """
    Calculates the Debt-to-Income (DTI) ratio.
    """
    if gross_monthly_income <= 0:
        return 0.0
    return total_monthly_debt / gross_monthly_income

# --- NEW FUNCTION FOR AUTOMATED CREDIT SCORE ---
def estimate_credit_score_category(gross_monthly_income, existing_monthly_debt_payments, calculated_dti_ratio):
    """
    Estimates a credit score category (Good, Average, Poor) based on financial inputs.
    This is a simplified heuristic and not a real credit score calculation.
    """
    if gross_monthly_income <= 0:
        return "Poor" # Cannot assess if no income

    # Existing debt as a percentage of income
    existing_debt_income_ratio = existing_monthly_debt_payments / gross_monthly_income

    # Heuristic rules based on DTI and existing debt burden
    if calculated_dti_ratio <= 0.30 and existing_debt_income_ratio <= 0.15:
        return "Good"
    elif calculated_dti_ratio <= 0.40 and existing_debt_income_ratio <= 0.30:
        return "Average"
    else:
        return "Poor"
# --- END NEW FUNCTION ---

def appraise_loan_application(
    loan_amount,
    annual_interest_rate_percent,
    loan_term_years,
    borrower_gross_monthly_income,
    existing_monthly_debt_payments,
    credit_score=None, # This parameter will now be populated by the automated function
    min_dti_for_approval=0.43,
    min_income_multiplier_for_loan=2.5
):
    """
    Appraises a loan application based on various criteria.
    """
    results = {
        "approved": False,
        "reasons": [],
        "monthly_payment_new_loan": 0.0,
        "total_monthly_debt": 0.0,
        "dti_ratio": 0.0,
        "loan_amount_to_annual_income_ratio": 0.0,
        "estimated_credit_score": credit_score # Store the estimated score for display
    }

    annual_interest_rate_decimal = annual_interest_rate_percent / 100.0
    loan_term_months = loan_term_years * 12

    monthly_payment_new_loan = calculate_monthly_payment(
        loan_amount, annual_interest_rate_decimal, loan_term_months
    )
    results["monthly_payment_new_loan"] = round(monthly_payment_new_loan, 2)

    if monthly_payment_new_loan <= 0 and loan_amount > 0:
        results["reasons"].append("Calculation Error: Monthly payment could not be determined or is zero for a non-zero loan amount.")
        return results

    total_monthly_debt = monthly_payment_new_loan + existing_monthly_debt_payments
    results["total_monthly_debt"] = round(total_monthly_debt, 2)

    dti_ratio = calculate_debt_to_income_ratio(
        borrower_gross_monthly_income, total_monthly_debt
    )
    results["dti_ratio"] = round(dti_ratio, 2)

    borrower_annual_income = borrower_gross_monthly_income * 12
    loan_amount_to_annual_income_ratio = 0.0
    if borrower_annual_income > 0:
        loan_amount_to_annual_income_ratio = loan_amount / borrower_annual_income
    results["loan_amount_to_annual_income_ratio"] = round(loan_amount_to_annual_income_ratio, 2)

    is_eligible = True

    if borrower_gross_monthly_income <= 0:
        is_eligible = False
        results["reasons"].append("Insufficient income: Borrower's gross monthly income is zero or negative.")
    elif borrower_gross_monthly_income < monthly_payment_new_loan * 1.5:
        results["reasons"].append(
            f"Income appears low relative to the proposed monthly payment (less than 1.5x). "
            f"Required: {round(monthly_payment_new_loan * 1.5, 2)} XAF. Provided: {borrower_gross_monthly_income} XAF."
        )
        is_eligible = False

    if dti_ratio > min_dti_for_approval:
        is_eligible = False
        results["reasons"].append(
            f"High Debt-to-Income (DTI) ratio: {dti_ratio * 100:.2f}%. "
            f"Exceeds maximum allowable DTI of {min_dti_for_approval * 100:.2f}%."
        )

    if borrower_annual_income > 0 and loan_amount_to_annual_income_ratio > min_income_multiplier_for_loan:
        is_eligible = False
        results["reasons"].append(
            f"Loan amount is too high relative to annual income ({loan_amount_to_annual_income_ratio:.2f}x). "
            f"Maximum recommended is {min_income_multiplier_for_loan:.1f}x annual income."
        )

    # --- Use the estimated credit score directly in appraisal logic ---
    if credit_score: # credit_score is now the estimated_credit_score_category
        if credit_score.lower() == "poor":
            is_eligible = False
            results["reasons"].append("Estimated credit score is Poor (based on financial profile), indicating high risk.")
        elif credit_score.lower() == "average" and dti_ratio > 0.36:
            is_eligible = False
            results["reasons"].append("Estimated credit score is Average with a DTI ratio over 36%, which is high risk.")
    # No 'else' for missing credit score because it's now always estimated

    if loan_term_years > 20:
        is_eligible = False
        results["reasons"].append("Loan term is excessively long (over 20 years).")

    if loan_amount < 100000:
        results["reasons"].append("Loan amount is below the minimum threshold (100,000 XAF).")

    if is_eligible and not results["reasons"]:
        results["approved"] = True
        results["reasons"].append("Loan application approved based on provided criteria.")
    elif not results["reasons"] and not is_eligible:
        results["reasons"].append("Loan application declined due to unspecified internal criteria.")
    elif is_eligible and results["reasons"]:
        results["approved"] = True
        results["reasons"].insert(0, "Loan application approved, but with some flagged concerns.")

    return results