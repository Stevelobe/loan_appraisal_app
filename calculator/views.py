# calculator/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .forms import (
    LoanTypeSelectionForm, MortgageLoanApplicationForm,
    SalaryBackedLoanApplicationForm, LoanWithinSavingsApplicationForm,
    LoanAboveSavingsApplicationForm, StandingOrderLoanApplicationForm,
    BaseLoanApplicationForm
)
from .models import (
    LoanApplication,
    MortgageLoanApplication, SalaryBackedLoanApplication,
    LoanWithinSavingsApplication, LoanAboveSavingsApplication,
    StandingOrderLoanApplication
)
from .appraisal_logic import (
    appraise_mortgage_loan, appraise_salary_backed_loan,
    appraise_loan_within_savings, appraise_loan_above_savings,
    appraise_standing_order_loan,
    calculate_monthly_payment
)
from decimal import Decimal
import csv
import re # <--- ADDED THIS IMPORT
from django.http import HttpResponse


def loan_type_selection_view(request):
    """
    Displays a page for the user to select the type of loan.
    Also calculates and displays the total number of loans granted.
    """
    total_approved_loans = LoanApplication.objects.filter(approved=True).count()
    
    # Fetch recent loan applications here for both GET and POST (if form invalid)
    recent_applications = LoanApplication.objects.all().order_by('-submission_date')[:5]

    if request.method == 'POST':
        form = LoanTypeSelectionForm(request.POST)
        if form.is_valid():
            loan_type = form.cleaned_data['loan_type']
            if loan_type == 'mortgage':
                return redirect('mortgage_loan_application')
            elif loan_type == 'salary_backed':
                return redirect('salary_backed_loan_application')
            elif loan_type == 'within_savings':
                return redirect('loan_within_savings_application')
            elif loan_type == 'above_savings':
                return redirect('loan_above_savings_application')
            elif loan_type == 'standing_order':
                return redirect('standing_order_loan_application')
            else:
                # Fallback if an invalid loan type somehow gets through
                context = {
                    'form': form,
                    'page_title': 'Select Loan Type',
                    'error_message': 'Invalid loan type selected.',
                    'total_approved_loans': total_approved_loans,
                    'recent_applications': recent_applications, # Pass recent apps
                }
                return render(request, 'calculator/loan_selection.html', context)
    else:
        form = LoanTypeSelectionForm()

    context = {
        'form': form,
        'page_title': 'Select Loan Type',
        'total_approved_loans': total_approved_loans,
        'recent_applications': recent_applications, # Always pass for initial load
    }
    return render(request, 'calculator/loan_selection.html', context)

# --- Generic Loan Application View Function ---
def _handle_loan_application(request, form_class, model_class, appraisal_func, loan_type_slug, loan_type_display_name, template_name):
    results = None
    form = form_class()

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            loan_app = form.save(commit=False)
            loan_app.loan_type = loan_type_slug
            
            appraisal_data = form.cleaned_data.copy()

            for field_name, field_value in form.fields.items():
                if isinstance(field_value, forms.FileField):
                    appraisal_data[field_name] = bool(request.FILES.get(field_name))
                elif isinstance(field_value, forms.BooleanField):
                    appraisal_data[field_name] = form.cleaned_data.get(field_name, False)
            
            appraisal_results = appraisal_func(appraisal_data)

            loan_app.appraisal_score = appraisal_results['score']
            # Store the raw reasons from appraisal_logic here for the model.
            # We'll format it for the template separately.
            loan_app.reasons = appraisal_results['reasons'] 
            loan_app.approved = appraisal_results['approved']

            loan_app.save()

            submitted_application_details = []
            
            submitted_application_details.append({'label': 'Applicant Name', 'value': loan_app.applicant_name})
            submitted_application_details.append({'label': 'Applicant Email', 'value': loan_app.applicant_email})
            submitted_application_details.append({'label': 'Loan Amount', 'value': f"{loan_app.loan_amount:,.0f} XAF"})
            submitted_application_details.append({'label': 'Interest Rate', 'value': f"{loan_app.annual_interest_rate_percent}%"})
            submitted_application_details.append({'label': 'Loan Term', 'value': f"{loan_app.loan_term_years} Years"})
            submitted_application_details.append({'label': 'Gross Monthly Income', 'value': f"{loan_app.borrower_gross_monthly_income:,.0f} XAF"})
            submitted_application_details.append({'label': 'Existing Monthly Debts', 'value': f"{loan_app.existing_monthly_debt_payments:,.0f} XAF"})
            
            submitted_application_details.append({'label': 'MFI Account Number', 'value': loan_app.account_number if loan_app.account_number else 'Not Provided'})
            submitted_application_details.append({'label': 'Current Savings Balance', 'value': f"{loan_app.savings_balance:,.0f}" if loan_app.savings_balance is not None else 'Not Provided'})


            kyc_fields_for_display = [
                'identity_card_number', 'place_of_birth', 'current_address',
                'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi',
                'profession'
            ]
            for field_name in kyc_fields_for_display:
                field = form.fields.get(field_name)
                if field:
                    value = form.cleaned_data.get(field_name)
                    display_value = str(value) if value is not None and value != '' else 'Not Provided'
                    submitted_application_details.append({
                        'label': field.label,
                        'value': display_value
                    })

            field = form.fields.get('loan_purpose_document')
            if field:
                display_value = ""
                # Check if a new file was uploaded for this submission
                if request.FILES.get('loan_purpose_document'):
                    display_value = "Uploaded (File Received)"
                # Check if there's an existing file associated with the loan_app instance
                elif getattr(loan_app, 'loan_purpose_document', None) and loan_app.loan_purpose_document.name:
                    display_value = f"Existing: {loan_app.loan_purpose_document.name.split('/')[-1]}"
                else:
                    display_value = "Not Uploaded"
                submitted_application_details.append({
                    'label': field.label,
                    'value': display_value
                })

            specific_form_fields_to_check = [
                f for f in form.Meta.fields if f not in BaseLoanApplicationForm.Meta.fields
            ]

            for field_name in specific_form_fields_to_check:
                field = form.fields.get(field_name)
                if field:
                    display_value = ""
                    if isinstance(field, forms.FileField):
                        if request.FILES.get(field_name):
                            display_value = "Uploaded (File Received)"
                        elif getattr(loan_app, field_name, None) and getattr(loan_app, field_name).name:
                            display_value = f"Existing: {getattr(loan_app, field_name).name.split('/')[-1]}"
                        else:
                            display_value = "Not Uploaded"
                    elif isinstance(field, forms.BooleanField):
                        checked_status = form.cleaned_data.get(field_name, False)
                        display_value = "Yes (System Verified)" if checked_status else "No (System Not Met)"
                    else:
                        value = form.cleaned_data.get(field_name)
                        display_value = str(value) if value is not None and value != '' else 'N/A'

                    submitted_application_details.append({
                        'label': field.label,
                        'value': display_value
                    })
            
            # --- CRITICAL FIX: Format reasons for the template as a list of dictionaries ---
            formatted_reasons = []
            for reason_str in appraisal_results['reasons']:
                status = 'info' # Default status
                description = reason_str
                points_awarded = None

                # Use regex to extract status and points
                # This regex now correctly handles optional points at the end
                match = re.match(r'^(✔|✖|ℹ️)\s*(.*?)(?:\s*\((?:[+-]?\d+\.?\d*)%?\s*points?\))?$', reason_str)
                if match:
                    prefix = match.group(1)
                    description = match.group(2).strip()
                    points_match = re.search(r'([+-]?\d+\.?\d*)%', reason_str) # Look for percentage points specifically
                    if points_match:
                        try:
                            points_awarded = float(points_match.group(1))
                        except ValueError:
                            pass # Keep as None if conversion fails

                    if prefix == '✔':
                        status = 'met'
                    elif prefix == '✖':
                        status = 'not_met'
                    elif prefix == 'ℹ️':
                        status = 'info'
                
                # Further refine description by removing the points part if present
                # This ensures the description passed to the template is clean
                description = re.sub(r'\s*\((?:[+-]?\d+\.?\d*)%?\s*points?\)$', '', description).strip()


                formatted_reasons.append({
                    'status': status,
                    'description': description,
                    'points_awarded': points_awarded
                })

            # Prepare results to be passed via session
            results_to_session = {
                'loan_type': loan_type_display_name,
                'applicant_name': loan_app.applicant_name,
                'score': appraisal_results['score'],
                'approved': appraisal_results['approved'],
                'reasons': formatted_reasons, # Use the newly formatted reasons
                'monthly_payment_new_loan': appraisal_results['monthly_payment_new_loan'],
                'total_monthly_debt': appraisal_results['total_monthly_debt'],
                'dti_ratio': appraisal_results['dti_ratio'],
                'dti_percentage': appraisal_results['dti_percentage'],
                'estimated_net_monthly_income': appraisal_results['estimated_net_monthly_income'],
                'loan_amount_to_annual_income_ratio': appraisal_results['loan_amount_to_annual_income_ratio'],
                'submitted_application_details': submitted_application_details,
            }
            
            # Store results in session and redirect to appraisal_results_view
            request.session['latest_appraisal_results'] = results_to_session
            return redirect('appraisal_results')

    context = {
        'form': form,
        'results': results, # This 'results' will be None for initial GET
        'page_title': loan_type_display_name + ' Application',
        'loan_type_display': loan_type_display_name
    }
    return render(request, template_name, context)

# --- Specific Loan Application Views (remains unchanged) ---

def mortgage_loan_application_view(request):
    return _handle_loan_application(
        request,
        MortgageLoanApplicationForm,
        MortgageLoanApplication,
        appraise_mortgage_loan,
        'mortgage',
        'Mortgage Loan',
        'calculator/mortgage_form.html'
    )

def salary_backed_loan_application_view(request):
    return _handle_loan_application(
        request,
        SalaryBackedLoanApplicationForm,
        SalaryBackedLoanApplication,
        appraise_salary_backed_loan,
        'salary_backed',
        'Salary-Backed Loan',
        'calculator/salary_backed_form.html'
    )

def loan_within_savings_application_view(request):
    return _handle_loan_application(
        request,
        LoanWithinSavingsApplicationForm,
        LoanWithinSavingsApplication,
        appraise_loan_within_savings,
        'within_savings',
        'Loan Within Savings',
        'calculator/loan_within_savings_form.html'
    )

def loan_above_savings_application_view(request):
    return _handle_loan_application(
        request,
        LoanAboveSavingsApplicationForm,
        LoanAboveSavingsApplication,
        appraise_loan_above_savings,
        'above_savings',
        'Loan Above Savings',
        'calculator/loan_above_savings_form.html'
    )

def standing_order_loan_application_view(request):
    return _handle_loan_application(
        request,
        StandingOrderLoanApplicationForm,
        StandingOrderLoanApplication,
        appraise_standing_order_loan,
        'standing_order',
        'Standing Order Loan',
        'calculator/standing_order_form.html'
    )

def appraisal_results_view(request):
    """
    Displays the results of a loan appraisal.
    """
    results = request.session.get('latest_appraisal_results')
    # Do NOT delete results from session here if you want it to persist across refreshes
    # for debugging. If you want it to be a one-time view, keep the del.
    # For now, I'll keep the del, as it's standard practice for one-time results.
    if results:
        del request.session['latest_appraisal_results']

    context = {
        'results': results,
        'page_title': 'Appraisal Results'
    }
    return render(request, 'calculator/appraisal_results.html', context)


def approved_loans_list_view(request):
    """
    Displays a table of all approved loans.
    """
    approved_loans = LoanApplication.objects.filter(approved=True).order_by('-submission_date')
    
    loans_data = []
    for index, loan in enumerate(approved_loans):
        monthly_installment = calculate_monthly_payment(
            loan.loan_amount,
            loan.annual_interest_rate_percent,
            loan.loan_term_years
        )
        
        loans_data.append({
            'id': loan.id, # <--- Add loan ID for deletion
            's_n': index + 1,
            'account_number': loan.account_number if loan.account_number else 'N/A',
            'applicant_name': loan.applicant_name,
            'loan_amount': f"{loan.loan_amount:,.0f}",
            'duration_years': loan.loan_term_years,
            'savings_balance': f"{loan.savings_balance:,.0f}" if loan.savings_balance is not None else 'N/A',
            'monthly_installment': f"{monthly_installment:,.2f}",
        })
    
    context = {
        'page_title': 'Approved Loans List',
        'loans': loans_data,
    }
    return render(request, 'calculator/approved_loans_list.html', context)


def export_approved_loans_csv(request):
    """
    Exports the list of approved loans to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="approved_loans.csv"'

    writer = csv.writer(response)
    
    writer.writerow([
        'S/N', 'Account Number', 'Name of Member', 'Loan Amount (XAF)',
        'Duration (Years)', 'Savings Balance (XAF)', 'Monthly Installment (XAF)'
    ])

    approved_loans = LoanApplication.objects.filter(approved=True).order_by('-submission_date')
    
    for index, loan in enumerate(approved_loans):
        monthly_installment = calculate_monthly_payment(
            loan.loan_amount,
            loan.annual_interest_rate_percent,
            loan.loan_term_years
        )
        writer.writerow([
            index + 1,
            loan.account_number if loan.account_number else 'N/A',
            loan.applicant_name,
            f"{loan.loan_amount:,.0f}".replace(',', ''),
            loan.loan_term_years,
            f"{loan.savings_balance:,.0f}".replace(',', '') if loan.savings_balance is not None else 'N/A',
            f"{monthly_installment:,.2f}".replace(',', ''),
        ])
    
    return response


def cobac_regulations_and_5cs_view(request):
    """
    Displays the COBAC regulations and 5 Cs of Credit appraisal elements.
    """
    context = {
        'page_title': 'COBAC Regulations & 5 Cs of Credit',
    }
    return render(request, 'calculator/cobac_regulations_and_5cs.html', context)

def delete_approved_loans(request):
    """
    Deletes selected approved loan applications.
    """
    print(f"Received delete request. Method: {request.method}") # DEBUG
    if request.method == 'POST':
        # Get list of IDs from checkboxes (these will be strings)
        loan_ids_str = request.POST.getlist('loan_ids')
        
        # Convert IDs from strings to integers
        loan_ids_to_delete = []
        for lid_str in loan_ids_str:
            try:
                loan_ids_to_delete.append(int(lid_str))
            except ValueError:
                print(f"DEBUG: Skipping invalid loan ID (not an integer): '{lid_str}'") # DEBUG
                pass # Skip any non-integer IDs
        
        print(f"DEBUG: Attempting to delete loans with IDs: {loan_ids_to_delete}") # DEBUG

        if loan_ids_to_delete:
            # Perform the deletion
            deleted_count, _ = LoanApplication.objects.filter(id__in=loan_ids_to_delete).delete()
            print(f"DEBUG: Successfully deleted {deleted_count} loan(s).") # DEBUG
            # Optional: Add Django messages for user feedback (requires setup in settings.py and base.html)
            # from django.contrib import messages
            # messages.success(request, f"{deleted_count} loan(s) deleted successfully.")
        else:
            print("DEBUG: No valid loan IDs received for deletion.") # DEBUG
            # messages.warning(request, "No loans selected for deletion.")
    else:
        print("DEBUG: Delete request was not a POST request (likely a direct URL access).") # DEBUG
    
    # Always redirect back to the approved loans list after deletion attempt
    return redirect('approved_loans_list')