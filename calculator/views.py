# calculator/views.py
from django.shortcuts import render
# Import all necessary functions/classes
from .appraisal_logic import (
    appraise_loan_application,
    calculate_monthly_payment, # Need this for DTI calc before appraise
    calculate_debt_to_income_ratio, # Need this for DTI calc before appraise
    estimate_credit_score_category # New function
)
from .forms import LoanApplicationForm
from .models import LoanApplication

def loan_appraisal_view(request):
    results = None
    form = LoanApplicationForm()

    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan_amount = float(form.cleaned_data['loan_amount'])
            annual_interest_rate_percent = float(form.cleaned_data['annual_interest_rate_percent'])
            loan_term_years = form.cleaned_data['loan_term_years']
            borrower_gross_monthly_income = float(form.cleaned_data['borrower_gross_monthly_income'])
            existing_monthly_debt_payments = float(form.cleaned_data['existing_monthly_debt_payments'])
            # credit_score is no longer directly from form.cleaned_data

            # --- AUTOMATED CREDIT SCORE INTEGRATION START ---
            # 1. Calculate new monthly payment and total monthly debt first to get DTI
            monthly_payment_new_loan_temp = calculate_monthly_payment(
                loan_amount, annual_interest_rate_percent / 100.0, loan_term_years * 12
            )
            total_monthly_debt_temp = monthly_payment_new_loan_temp + existing_monthly_debt_payments
            calculated_dti_ratio_temp = calculate_debt_to_income_ratio(
                borrower_gross_monthly_income, total_monthly_debt_temp
            )

            # 2. Estimate credit score category based on these intermediate calculations
            estimated_credit_score_category = estimate_credit_score_category(
                borrower_gross_monthly_income,
                existing_monthly_debt_payments,
                calculated_dti_ratio_temp
            )
            # --- AUTOMATED CREDIT SCORE INTEGRATION END ---

            # Now pass the estimated credit score to the main appraisal function
            appraisal_results = appraise_loan_application(
                loan_amount=loan_amount,
                annual_interest_rate_percent=annual_interest_rate_percent,
                loan_term_years=loan_term_years,
                borrower_gross_monthly_income=borrower_gross_monthly_income,
                existing_monthly_debt_payments=existing_monthly_debt_payments,
                credit_score=estimated_credit_score_category # Pass the estimated score
            )
            
            # Add the estimated credit score to results for display
            appraisal_results['estimated_credit_score'] = estimated_credit_score_category
            appraisal_results['dti_percentage'] = round(appraisal_results['dti_ratio'] * 100, 1)

            results = appraisal_results

            try:
                loan_app = LoanApplication(
                    loan_amount=loan_amount,
                    annual_interest_rate_percent=annual_interest_rate_percent,
                    loan_term_years=loan_term_years,
                    borrower_gross_monthly_income=borrower_gross_monthly_income,
                    existing_monthly_debt_payments=existing_monthly_debt_payments,
                    # Save the estimated credit score to the model
                    credit_score=estimated_credit_score_category,
                    approved=results['approved'],
                    reasons=results['reasons'],
                    monthly_payment_new_loan=results['monthly_payment_new_loan'],
                    total_monthly_debt=results['total_monthly_debt'],
                    dti_ratio=results['dti_ratio'],
                    loan_amount_to_annual_income_ratio=results['loan_amount_to_annual_income_ratio']
                )
                loan_app.save()
            except Exception as e:
                print(f"Error saving loan application: {e}")

    context = {
        'form': form,
        'results': results
    }
    return render(request, 'calculator/appraisal_form.html', context)