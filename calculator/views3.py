from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.apps import apps # Import apps to dynamically get models
from decimal import Decimal # Import Decimal for comparisons
from django.http import HttpResponse
# Imports for PDF generation
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io # For handling byte streams

# NEW IMPORTS FOR AUTHENTICATION
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# NEW IMPORT for appraisal logic - ALL APPRAISAL FUNCTIONS INCLUDED
from .appraisal_logic import (
    appraise_mortgage_loan,
    appraise_business_loan,
    appraise_salary_backed_loan,
    appraise_loan_within_savings,
    appraise_daily_savings_loan,
    appraise_standing_order_loan,
    appraise_real_estate_loan,
    appraise_container_loan,
    appraise_agricultural_loan,
    appraise_express_loan,
    APPROVAL_THRESHOLD,
    BOARD_REVIEW_THRESHOLD
)


from .forms import (
    LoanTypeSelectionForm,
    MortgageLoanApplicationForm,
    SalaryBackedLoanApplicationForm,
    LoanWithinSavingsApplicationForm,
    DailySavingsLoanApplicationForm,
    StandingOrderLoanApplicationForm,
    RealEstateLoanApplicationForm,
    ContainerLoanApplicationForm,
    AgriculturalLoanApplicationForm,
    ExpressLoanApplicationForm,
    BusinessLoanApplicationForm,
    UserRegistrationForm,
    UserLoginForm,
)
from .models import (
    LoanApplication, # Base model
    MortgageLoanApplication,
    SalaryBackedLoanApplication,
    LoanWithinSavingsApplication,
    DailySavingsLoanApplication,
    StandingOrderLoanApplication,
    RealEstateLoanApplication,
    ContainerLoanApplication,
    AgriculturalLoanApplication,
    ExpressLoanApplication,
    BusinessLoanApplication,
)

# --- NEW AUTHENTICATION VIEWS ---
def signup_view(request):
    """
    Handles user registration.
    If POST request and form is valid, creates a new user, logs them in,
    and redirects to the loan selection page.
    Otherwise, displays the signup form with errors or as a new empty form.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after signup
            messages.success(request, "Registration successful. Welcome!")
            return redirect('loan_selection') # Redirect to your main app page
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    """
    Handles user login.
    If POST request and credentials are valid, authenticates and logs in the user,
    then redirects to the loan selection page.
    Otherwise, displays the login form with errors or as a new empty form.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('loan_selection') # Redirect to your main app page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required # This decorator ensures only logged-in users can access this view
def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    Requires the user to be logged in to access this view.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login') # Redirect to the login page

# --- Helper function to get total approved loans and recent applications ---
# Apply @login_required to views that require authentication
@login_required
def get_dashboard_data(request):
    """
    Fetches the total count of approved loans and the 5 most recent loan applications
    SPECIFIC TO THE CURRENTLY LOGGED-IN USER.
    """
    # Filter by the current user (request.user)
    # IMPORTANT: Ensure your LoanApplication model has a ForeignKey to User (e.g., 'user' or 'applicant')
    # If your field is named 'applicant', change 'user=request.user' to 'applicant=request.user'
    user_loans = LoanApplication.objects.filter(user=request.user)

    total_approved_loans = user_loans.filter(approved=True).count()

    # Fetch recent applications for the current user
    recent_applications = user_loans.order_by('-submission_date')[:5]

    return total_approved_loans, recent_applications

# --- Automated Appraisal Logic ---
def perform_automated_appraisal(loan_instance):
    """
    Performs an automated appraisal by calling the appropriate appraisal logic
    from appraisal_logic.py based on the loan type.
    """
    appraisal_results = {}

    # Convert loan_instance data to a dictionary for appraisal_logic functions
    # This assumes that the appraisal_logic functions expect a dictionary input
    # and that the loan_instance attributes match the keys expected by appraisal_logic.
    # For FileFields like land_title_document, check if they have a value (e.g., .name)
    loan_data = {
        'loan_amount': loan_instance.loan_amount,
        'annual_interest_rate_percent': loan_instance.annual_interest_rate_percent,
        'loan_term_years': loan_instance.loan_term_years,
        'borrower_gross_monthly_income': loan_instance.borrower_gross_monthly_income,
        'existing_monthly_debt_payments': loan_instance.existing_monthly_debt_payments,
        'loan_purpose_document': loan_instance.loan_purpose, # Pass base loan_purpose as loan_purpose_document
        'identity_card_number': loan_instance.identity_card_number,
        'place_of_birth': loan_instance.place_of_birth,
        'current_address': loan_instance.current_address,
        'marital_status': loan_instance.marital_status,
        'duration_with_mfi_years': loan_instance.duration_with_mfi_years,
        'num_loans_other_mfi': loan_instance.num_loans_other_mfi,
        'profession': loan_instance.profession,
    }

    # Add specific fields based on loan type
    if loan_instance.loan_type == 'mortgage':
        # Access the related MortgageLoanApplication instance
        try:
            mortgage_specific_data = loan_instance.mortgageloanapplication
            loan_data['land_title_document'] = bool(mortgage_specific_data.land_title_document)
            loan_data['power_of_attorney_document'] = bool(mortgage_specific_data.power_of_attorney_document)
            loan_data['legal_mortgage_agreement_document'] = bool(mortgage_specific_data.legal_mortgage_agreement_document)
            loan_data['supporting_documents'] = bool(mortgage_specific_data.supporting_documents)
            loan_data['no_existing_npl'] = mortgage_specific_data.no_existing_npl
            appraisal_results = appraise_mortgage_loan(loan_data)
        except MortgageLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Mortgage specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_ratio': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'business':
        # Access the related BusinessLoanApplication instance
        try:
            business_specific_data = loan_instance.businessloanapplication
            loan_data['valid_source_of_income_for_repayment'] = business_specific_data.valid_source_of_income_for_repayment
            loan_data['savings_balance_ge_20_percent_loan'] = business_specific_data.savings_balance_ge_20_percent_loan
            loan_data['cost_estimate_provided'] = business_specific_data.cost_estimate_provided
            loan_data['land_documents_attached'] = bool(business_specific_data.land_documents_attached) # Assuming this is a FileField
            appraisal_results = appraise_business_loan(loan_data)
        except BusinessLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Business specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0}

    elif loan_instance.loan_type == 'salary_backed':
        try:
            salary_backed_specific_data = loan_instance.salarybackedloanapplication
            loan_data['salary_passing_union_ge_3_months'] = salary_backed_specific_data.salary_passing_union_ge_3_months
            loan_data['savings_ge_1_10_loan'] = salary_backed_specific_data.savings_ge_1_10_loan
            loan_data['copy_of_effective_service_document'] = bool(salary_backed_specific_data.copy_of_effective_service_document)
            loan_data['irrevocable_salary_transfer_document'] = bool(salary_backed_specific_data.irrevocable_salary_transfer_document)
            appraisal_results = appraise_salary_backed_loan(loan_data)
        except SalaryBackedLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Salary-backed specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'within_savings':
        try:
            savings_specific_data = loan_instance.loanwithinsavingsapplication
            loan_data['savings_covers_loan_plus_interest'] = savings_specific_data.savings_covers_loan_plus_interest
            loan_data['loan_amount_blocked_in_savings'] = savings_specific_data.loan_amount_blocked_in_savings
            loan_data['no_active_default'] = savings_specific_data.no_active_default
            appraisal_results = appraise_loan_within_savings(loan_data)
        except LoanWithinSavingsApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Loan Within Savings specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'daily_savings':
        try:
            daily_savings_specific_data = loan_instance.dailysavingsloanapplication
            loan_data['daily_savings_active_ge_6_months'] = daily_savings_specific_data.daily_savings_active_ge_6_months
            loan_data['signed_deduction_agreement_document'] = bool(daily_savings_specific_data.signed_deduction_agreement_document)
            loan_data['valid_surety_bond_document'] = bool(daily_savings_specific_data.valid_surety_bond_document)
            loan_data['positive_loan_repayment_history'] = daily_savings_specific_data.positive_loan_repayment_history
            loan_data['savings_balance_ge_1_5_loan'] = daily_savings_specific_data.savings_balance_ge_1_5_loan
            appraisal_results = appraise_daily_savings_loan(loan_data)
        except DailySavingsLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Daily Savings specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'standing_order':
        try:
            standing_order_specific_data = loan_instance.standingorderloanapplication
            loan_data['standing_order_active_ge_3_months'] = standing_order_specific_data.standing_order_active_ge_3_months
            loan_data['loan_duration_le_1_year'] = standing_order_specific_data.loan_duration_le_1_year
            loan_data['savings_balance_ge_1_5_loan'] = standing_order_specific_data.savings_balance_ge_1_5_loan
            loan_data['no_existing_default_or_delinquency'] = standing_order_specific_data.no_existing_default_or_delinquency
            appraisal_results = appraise_standing_order_loan(loan_data)
        except StandingOrderLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Standing Order specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'real_estate':
        try:
            real_estate_specific_data = loan_instance.realestateloanapplication
            loan_data['loan_duration_ge_10_years'] = real_estate_specific_data.loan_duration_ge_10_years
            loan_data['loan_amount_le_10_percent_paid_up_capital'] = real_estate_specific_data.loan_amount_le_10_percent_paid_up_capital
            loan_data['legal_mortgage_agreement_document_re'] = bool(real_estate_specific_data.legal_mortgage_agreement_document_re)
            loan_data['land_title_in_borrowers_name'] = real_estate_specific_data.land_title_in_borrowers_name
            loan_data['valid_proof_of_source_of_income'] = real_estate_specific_data.valid_proof_of_source_of_income
            appraisal_results = appraise_real_estate_loan(loan_data)
        except RealEstateLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Real Estate specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'container':
        try:
            container_specific_data = loan_instance.containerloanapplication
            loan_data['bill_of_lading_document'] = bool(container_specific_data.bill_of_lading_document)
            loan_data['custom_clearance_plan_document'] = bool(container_specific_data.custom_clearance_plan_document)
            # Note: savings_balance_amount is passed directly to appraisal_logic, but the boolean is also needed for scoring.
            loan_data['savings_balance_amount'] = container_specific_data.savings_balance_amount
            loan_data['savings_balance_ge_1_5_loan'] = container_specific_data.savings_balance_ge_1_5_loan
            loan_data['valid_proof_of_source_of_income'] = container_specific_data.valid_proof_of_source_of_income
            appraisal_results = appraise_container_loan(loan_data)
        except ContainerLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Container specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'agricultural':
        try:
            agricultural_specific_data = loan_instance.agriculturalloanapplication
            loan_data['is_land_personal_belonging'] = agricultural_specific_data.is_land_personal_belonging
            loan_data['has_authorization_of_usage'] = agricultural_specific_data.has_authorization_of_usage
            loan_data['loan_purpose_category'] = agricultural_specific_data.loan_purpose_category
            loan_data['savings_balance_amount'] = agricultural_specific_data.savings_balance_amount
            loan_data['savings_balance_ge_1_5_loan'] = agricultural_specific_data.savings_balance_ge_1_5_loan
            loan_data['total_cost_estimate_document'] = bool(agricultural_specific_data.total_cost_estimate_document)
            loan_data['valid_proof_of_source_of_income'] = agricultural_specific_data.valid_proof_of_source_of_income
            appraisal_results = appraise_agricultural_loan(loan_data)
        except AgriculturalLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Agricultural specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    elif loan_instance.loan_type == 'express':
        try:
            express_specific_data = loan_instance.expressloanapplication
            loan_data['salary_deducted_at_source_or_standing_order'] = express_specific_data.salary_deducted_at_source_or_standing_order
            loan_data['effective_service_available'] = express_specific_data.effective_service_available
            loan_data['clearly_valid_purpose_of_loan'] = express_specific_data.clearly_valid_purpose_of_loan
            loan_data['savings_balance_amount'] = express_specific_data.savings_balance_amount
            loan_data['savings_balance_ge_1_10_loan'] = express_specific_data.savings_balance_ge_1_10_loan
            loan_data['no_existing_delinquent_loan'] = express_specific_data.no_existing_delinquent_loan
            appraisal_results = appraise_express_loan(loan_data)
        except ExpressLoanApplication.DoesNotExist:
            appraisal_results = {'score': 0.0, 'approved': False, 'reasons': ["Express specific data missing."], 'monthly_payment_new_loan': 0.0, 'total_monthly_debt': 0.0, 'dti_percentage': 0.0, 'estimated_net_monthly_income': 0.0, 'loan_amount_to_annual_income_ratio': 0.0}

    else:
        # Fallback for unhandled loan types or a general appraisal if needed
        # For now, we'll set it to a default "needs review" state
        appraisal_results = {
            'score': 0.0,
            'approved': None, # Indicates needs review
            'reasons': [f"Appraisal logic not yet implemented for loan type: {loan_instance.loan_type}"],
            'monthly_payment_new_loan': 0.0,
            'total_monthly_debt': 0.0,
            'dti_percentage': 0.0,
            'estimated_net_monthly_income': 0.0
        }

    # Update the loan_instance with results from the appraisal logic
    loan_instance.appraisal_score = Decimal(str(appraisal_results.get('score', 0.0)))
    loan_instance.approved = appraisal_results.get('approved', None)
    loan_instance.reasons = appraisal_results.get('reasons', [])

    # Determine approver_comments based on the appraisal_logic's decision
    if loan_instance.approved is True:
        loan_instance.approver_comments = "Automated approval based on appraisal logic."
    elif loan_instance.approved is False:
        loan_instance.approver_comments = "Automated rejection based on appraisal logic."
    else: # None, meaning needs board review
        loan_instance.approver_comments = "Requires manual board review based on appraisal logic."

    loan_instance.save() # Save the updated appraisal fields

# --- Main Loan Selection View ---
@login_required # Protect this view
def loan_selection_view(request):
    """
    Handles displaying the loan selection form (GET)
    and processing its submission (POST), then redirecting.
    Only accessible by logged-in users.
    """
    # Pass the 'request' object to get_dashboard_data()
    total_approved_loans, recent_applications = get_dashboard_data(request)

    if request.method == 'POST':
        form = LoanTypeSelectionForm(request.POST)
        if form.is_valid():
            loan_type = form.cleaned_data['loan_type']

            loan_redirects = {
                'mortgage': 'mortgage_loan_application',
                'salary_backed': 'salary_backed_loan_application',
                'within_savings': 'loan_within_savings_application',
                'daily_savings': 'daily_savings_loan_application',
                'standing_order': 'standing_order_loan_application',
                'real_estate': 'real_estate_loan_application',
                'container': 'container_loan_application',
                'agricultural': 'agricultural_loan_application',
                'express': 'express_loan_application',
                'business': 'business_loan_application',
            }

            url_name = loan_redirects.get(loan_type)

            if url_name:
                return redirect(reverse(url_name))
            else:
                messages.error(request, "Selected loan type is not recognized.")
                return redirect(reverse('loan_selection'))
        else:
            context = {
                'form': form,
                'total_approved_loans': total_approved_loans,
                'recent_applications': recent_applications,
            }
            return render(request, 'calculator/loan_selection.html', context)
    else: # This handles GET requests
        form = LoanTypeSelectionForm()
        context = {
            'form': form,
            'total_approved_loans': total_approved_loans,
            'recent_applications': recent_applications,
        }
        return render(request, 'calculator/loan_selection.html', context)

# --- Individual Loan Application Views (with automated appraisal) ---

# Helper to reduce repetition in loan application views
def _process_loan_application(request, form_class, loan_type_code, loan_type_display, template_name):
    """
    Helper function to process individual loan application forms.
    Handles form validation, saving the loan instance, and triggering automated appraisal.
    """
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            loan_instance = form.save(commit=False)
            loan_instance.loan_type = loan_type_code
            # Assign the current user to the loan application
            # IMPORTANT: Ensure your LoanApplication model has a 'user' field (ForeignKey to User)
            loan_instance.user = request.user
            loan_instance.save()

            # The form.save() for subclass forms handles specific fields.
            # No special handling needed for loan_purpose as it's now a TextField
            # and handled by form.save() directly.

            # --- Perform Automated Appraisal ---
            perform_automated_appraisal(loan_instance)

            messages.success(request, f"{loan_type_display} application submitted and appraised automatically!")
            return redirect(reverse('appraisal_results'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = form_class()
    return render(request, template_name, {'form': form, 'loan_type': loan_type_display})

# Apply @login_required to all loan application views
@login_required
def mortgage_loan_application(request): # Renamed for consistency with URL names
    """View for Mortgage Loan application. Requires login."""
    return _process_loan_application(request, MortgageLoanApplicationForm, 'mortgage', 'Mortgage Loan', 'calculator/mortgage_form.html')

@login_required
def salary_backed_loan_application(request): # Renamed
    """View for Salary-Backed Loan application. Requires login."""
    return _process_loan_application(request, SalaryBackedLoanApplicationForm, 'salary_backed', 'Salary-Backed Loan', 'calculator/salary_backed_form.html')

@login_required
def loan_within_savings_application(request): # Renamed
    """View for Loan Within Savings application. Requires login."""
    return _process_loan_application(request, LoanWithinSavingsApplicationForm, 'within_savings', 'Loan Within Savings', 'calculator/loan_within_savings_form.html')

@login_required
def daily_savings_loan_application(request): # Renamed
    """View for Daily Savings Loan application. Requires login."""
    return _process_loan_application(request, DailySavingsLoanApplicationForm, 'daily_savings', 'Daily Savings Loan', 'calculator/daily_savings_loan_form.html')

@login_required
def standing_order_loan_application(request): # Renamed
    """View for Standing Order Loan application. Requires login."""
    return _process_loan_application(request, StandingOrderLoanApplicationForm, 'standing_order', 'Standing Order Loan', 'calculator/standing_order_form.html')

@login_required
def real_estate_loan_application(request): # Renamed
    """View for Real Estate Loan application. Requires login."""
    return _process_loan_application(request, RealEstateLoanApplicationForm, 'real_estate', 'Real Estate Loan', 'calculator/real_estate_form.html')

@login_required
def container_loan_application(request): # Renamed
    """View for Container Loan application. Requires login."""
    return _process_loan_application(request, ContainerLoanApplicationForm, 'container', 'Container Loan', 'calculator/container_form.html')

@login_required
def agricultural_loan_application(request): # Renamed
    """View for Agricultural Loan application. Requires login."""
    return _process_loan_application(request, AgriculturalLoanApplicationForm, 'agricultural', 'Agricultural Loan', 'calculator/agricultural_form.html')

@login_required
def express_loan_application(request): # Renamed
    """View for Express Loan application. Requires login."""
    return _process_loan_application(request, ExpressLoanApplicationForm, 'express', 'Express Loan', 'calculator/express_form.html')

@login_required
def business_loan_application(request): # View for Business Loan application
    """View for Business Loan application. Requires login."""
    return _process_loan_application(request, BusinessLoanApplicationForm, 'business', 'Business Loan', 'calculator/business_form.html')


# --- Other existing views (updated to query LoanApplication directly) ---
@login_required # Protect this view
def appraisal_results_display_view(request):
    """
    Displays a list of all appraised loan applications for the current user. Requires login.
    """
    # Fetch all LoanApplication instances that have been appraised for the current user
    all_appraised_loans = LoanApplication.objects.filter(
        user=request.user, # <--- Filter by current user
        appraisal_score__isnull=False
    ).order_by('-submission_date')

    context = {
        'appraised_loans': all_appraised_loans
    }
    return render(request, 'calculator/appraisal_results.html', context)

@login_required # Protect this view
def approved_loans_list(request):
    """
    Displays a list of all approved loan applications for the current user. Requires login.
    """
    # Fetch all LoanApplication instances that are approved for the current user
    approved_loans = LoanApplication.objects.filter(
        user=request.user, # <--- Filter by current user
        approved=True
    ).order_by('-submission_date')

    context = {
        'approved_loans': approved_loans
    }
    return render(request, 'calculator/approved_loans_list.html', context)

@login_required # Protect this view
def cobac_regulations_and_5cs_view(request):
    """
    Displays information about COBAC regulations and the 5 Cs of credit. Requires login.
    """
    # Your logic for COBAC regulations
    return render(request, 'calculator/cobac_regulations_and_5cs.html', {})

@login_required # Protect this view
def loan_review_dashboard(request):
    """
    Displays a dashboard of loans currently under review (not yet appraised) for the current user. Requires login.
    """
    # Loans under review are those that haven't been appraised yet (appraisal_score is null) for the current user
    loans_under_review = LoanApplication.objects.filter(
        user=request.user, # <--- Filter by current user
        appraisal_score__isnull=True
    ).order_by('-submission_date')

    context = {
        'loans_under_review': loans_under_review
    }
    return render(request, 'calculator/loan_review_dashboard.html', context)


# --- New View: Download Appraisal PDF ---
@login_required # Protect this view
def download_appraisal_pdf(request, pk):
    """
    Generates and allows downloading of a PDF appraisal report for a specific loan. Requires login.
    """
    # Ensure the loan belongs to the current user for security
    loan = get_object_or_404(LoanApplication, pk=pk, user=request.user) # <--- Added user filter

    # Dynamically get the specific loan type instance
    specific_loan_instance = None
    if loan.loan_type == 'mortgage':
        specific_loan_instance = loan.mortgageloanapplication
    elif loan.loan_type == 'salary_backed':
        specific_loan_instance = loan.salarybackedloanapplication
    elif loan.loan_type == 'within_savings':
        specific_loan_instance = loan.loanwithinsavingsapplication
    elif loan.loan_type == 'daily_savings':
        specific_loan_instance = loan.dailysavingsloanapplication
    elif loan.loan_type == 'standing_order':
        specific_loan_instance = loan.standingorderloanapplication
    elif loan.loan_type == 'real_estate':
        specific_loan_instance = loan.realestateloanapplication
    elif loan.loan_type == 'container':
        specific_loan_instance = loan.containerloanapplication
    elif loan.loan_type == 'agricultural':
        specific_loan_instance = loan.agriculturalloanapplication
    elif loan.loan_type == 'express':
        specific_loan_instance = loan.expressloanapplication
    elif loan.loan_type == 'business':
        specific_loan_instance = loan.businessloanapplication

    context = {
        'loan': loan,
        'specific_loan': specific_loan_instance,
    }

    # Using your existing appraisal_results_pdf.html
    template = get_template('calculator/appraisal_results_pdf.html')
    html = template.render(context)

    result = io.BytesIO()
    pdf = pisa.CreatePDF(
        html,           # the HTML to convert
        dest=result,    # file handle to receive result
        encoding="UTF-8" # ensure correct encoding
    )
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="loan_appraisal_{loan.pk}.pdf"'
        return response
    return HttpResponse('We had some errors <pre>%s</pre>' % html)

# --- View to handle deleting approved loans ---
@login_required # Protect this view
def delete_approved_loans(request):
    """
    Handles the deletion of selected approved loan applications for the current user. Requires login.
    """
    if request.method == 'POST':
        selected_loan_ids = request.POST.getlist('selected_loans')
        if selected_loan_ids:
            # Delete selected loans, ensuring they belong to the current user
            deleted_count, _ = LoanApplication.objects.filter(
                pk__in=selected_loan_ids,
                user=request.user # <--- Added user filter for security
            ).delete()
            messages.success(request, f"{deleted_count} approved loan(s) deleted successfully.")
        else:
            messages.warning(request, "No loans selected for deletion.")
    return redirect(reverse('approved_loans_list'))

# --- View to display details of a single loan application (kept for compatibility, though not linked from dashboard) ---
@login_required # Protect this view
def loan_detail_view(request, pk):
    """
    Displays the detailed information for a single loan application for the current user. Requires login.
    """
    # Ensure the loan belongs to the current user for security
    loan = get_object_or_404(LoanApplication, pk=pk, user=request.user) # <--- Added user filter

    # Dynamically get the specific loan type instance
    specific_loan_instance = None
    if loan.loan_type == 'mortgage':
        specific_loan_instance = loan.mortgageloanapplication
    elif loan.loan_type == 'salary_backed':
        specific_loan_instance = loan.salarybackedloanapplication
    elif loan.loan_type == 'within_savings':
        specific_loan_instance = loan.loanwithinsavingsapplication
    elif loan.loan_type == 'daily_savings':
        specific_loan_instance = loan.dailysavingsloanapplication
    elif loan.loan_type == 'standing_order':
        specific_loan_instance = loan.standingorderloanapplication
    elif loan.loan_type == 'real_estate':
        specific_loan_instance = loan.realestateloanapplication
    elif loan.loan_type == 'container':
        specific_loan_instance = loan.containerloanapplication
    elif loan.loan_type == 'agricultural':
        specific_loan_instance = loan.agriculturalloanapplication
    elif loan.loan_type == 'express':
        specific_loan_instance = loan.expressloanapplication
    elif loan.loan_type == 'business':
        specific_loan_instance = loan.businessloanapplication

    context = {
        'loan': loan,
        'specific_loan': specific_loan_instance,
    }
    return render(request, 'calculator/loan_detail.html', context)

# --- NEW: Manual Loan Approval View ---
@login_required # Protect this view
def approve_loan(request, pk):
    """
    Manually approves a loan application for the current user. Requires login.
    This view should be accessed via a POST request.
    """
    # Ensure the loan belongs to the current user for security
    loan = get_object_or_404(LoanApplication, pk=pk, user=request.user) # <--- Added user filter
    if request.method == 'POST':
        loan.approved = True
        loan.appraisal_score = Decimal('100.00') # Set to a high score for manual approval
        loan.approver_comments = "Manually approved by reviewer."
        loan.reasons = [] # Clear any previous reasons for rejection
        loan.save()
        messages.success(request, f"Loan application {loan.pk} for {loan.applicant_name} has been approved.")
        return redirect(reverse('approved_loans_list')) # Redirect to approved list
    messages.info(request, "To approve, please submit a POST request (e.g., via a form button).")
    return redirect(reverse('loan_detail_view', kwargs={'pk': pk})) # Redirect back to detail or review dashboard

# --- NEW: Manual Loan Decline View ---
@login_required # Protect this view
def decline_loan(request, pk):
    """
    Manually declines a loan application for the current user. Requires login.
    This view should be accessed via a POST request.
    """
    # Ensure the loan belongs to the current user for security
    loan = get_object_or_404(LoanApplication, pk=pk, user=request.user) # <--- Added user filter
    if request.method == 'POST':
        loan.approved = False
        loan.appraisal_score = Decimal('0.00') # Set to a low score for manual decline
        loan.approver_comments = "Manually declined by reviewer."
        # Add a reason for manual decline if not already present
        if "Manually declined by reviewer." not in loan.reasons:
            loan.reasons.append("Manually declined by reviewer.")
        loan.save()
        messages.warning(request, f"Loan application {loan.pk} for {loan.applicant_name} has been declined.")
        return redirect(reverse('appraisal_results')) # Redirect to appraisal results (which shows both approved/declined)
    messages.info(request, "To decline, please submit a POST request (e.g., via a form button).")
    return redirect(reverse('loan_detail_view', kwargs={'pk': pk})) # Redirect back to detail or review dashboard
