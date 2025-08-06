# calculator/forms.py

from django import forms
from .models import (
    LoanApplication,
    MortgageLoanApplication,
    SalaryBackedLoanApplication,
    LoanWithinSavingsApplication,
    DailySavingsLoanApplication,
    StandingOrderLoanApplication,
    RealEstateLoanApplication,
    ContainerLoanApplication,
    AgriculturalLoanApplication,
    ExpressLoanApplication,
    BusinessLoanApplication, # NEW: Import the BusinessLoanApplication model
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import datetime

# NEW IMPORTS FOR AUTHENTICATION
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User # Django's built-in User model

# Define choices for marital status
MARITAL_STATUS_CHOICES = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
    ('widowed', 'Widowed'),
    ('separated', 'Separated'),
    ('other', 'Other'),
]

# Define choices for agricultural loan purpose (from your models.py)
AGRICULTURAL_LOAN_PURPOSE_CHOICES = [
    ('crops', 'Crops (e.g., maize, cassava, cocoa)'),
    ('livestock', 'Livestock (e.g., cattle, poultry, pigs)'),
]


# Base form for common loan application fields
# Define common CSS classes to avoid repetition
WIDGET_CLASS = 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out'

class BaseLoanApplicationForm(forms.ModelForm):
    # Override the marital_status field to include choices
    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': WIDGET_CLASS}),
        label="Marital Status",
        required=False
    )

    # Override the current_location field and set its label directly
    current_location = forms.CharField(
        label="Current City",  # Set the desired label here
        widget=forms.TextInput(attrs={'class': WIDGET_CLASS}),
    )

    class Meta:
        model = LoanApplication
        fields = [
            'applicant_name', 'applicant_email', 'loan_amount',
            'annual_interest_rate_percent', 'loan_term_years',
            'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'loan_purpose',
            'account_number', 'date_of_loan', 'current_location',
            'identity_card_number', 'place_of_birth', 'current_address',
            'marital_status',
            'duration_with_mfi_years', 'num_loans_other_mfi',
            'profession',
            'date_of_birth',
        ]
        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': WIDGET_CLASS}),
            'applicant_email': forms.EmailInput(attrs={'class': WIDGET_CLASS}),
            'loan_amount': forms.NumberInput(attrs={'class': WIDGET_CLASS, 'min': '0'}),
            'annual_interest_rate_percent': forms.NumberInput(attrs={'class': WIDGET_CLASS, 'min': '0', 'step': '0.01'}),
            'loan_term_years': forms.NumberInput(attrs={'class': WIDGET_CLASS, 'min': '0', 'step': '1'}),
            'borrower_gross_monthly_income': forms.NumberInput(attrs={'class': WIDGET_CLASS, 'min': '0'}),
            'existing_monthly_debt_payments': forms.NumberInput(attrs={'class': WIDGET_CLASS, 'min': '0'}),
            'loan_purpose': forms.Textarea(attrs={'class': WIDGET_CLASS, 'rows': 3}),
            'account_number': forms.TextInput(attrs={'class': WIDGET_CLASS}),
            'date_of_loan': forms.DateInput(attrs={'type': 'date', 'class': WIDGET_CLASS}),
            # The current_location widget is now handled by the field's explicit definition above
            'identity_card_number': forms.TextInput(attrs={'class': WIDGET_CLASS}),
            'place_of_birth': forms.TextInput(attrs={'class': WIDGET_CLASS}),
            'current_address': forms.TextInput(attrs={'class': WIDGET_CLASS}),
            'duration_with_mfi_years': forms.NumberInput(attrs={'class': WIDGET_CLASS, 'min': '0', 'step': '1'}),
            'num_loans_other_mfi': forms.NumberInput(attrs={'class': WIDGET_CLASS, 'min': '0', 'step': '1'}),
            'profession': forms.TextInput(attrs={'class': WIDGET_CLASS}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': WIDGET_CLASS}),
        }
        labels = {
            # Removed current_location here because the label is now set on the field itself.
            'date_of_birth': 'Date of Birth',
        }

# Loan Type Selection Form (remains unchanged)
class LoanTypeSelectionForm(forms.Form):
    LOAN_TYPES = [
        ('mortgage', 'Mortgage Loan'),
        ('salary_backed', 'Salary-Backed Loan'),
        ('within_savings', 'Loan Within Savings'),
        ('daily_savings', 'Daily Savings Loan'),
        ('standing_order', 'Standing Order Loan'),
        ('real_estate', 'Real Estate Loan'),
        ('container', 'Container Loan'),
        ('agricultural', 'Agricultural Loan'),
        ('express', 'Express Loan'),
        ('business', 'Business Loan'), # NEW: Added Business Loan Type
    ]
    loan_type = forms.ChoiceField(
        choices=LOAN_TYPES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out'}),
        label="Select Loan Type"
    )

# Specific Loan Application Forms inheriting from BaseLoanApplicationForm
# These forms will implicitly handle the one-to-one relationship with LoanApplication
# by saving their specific fields and linking to the base LoanApplication instance.
class MortgageLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = MortgageLoanApplication
        # Ensure that BaseLoanApplicationForm.Meta.fields is correctly extended
        fields = BaseLoanApplicationForm.Meta.fields + [
            'land_title_document', 'legal_mortgage_agreement_document',
            'power_of_attorney_document', 'supporting_documents', 'no_existing_npl'
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy() # Use .copy() to avoid modifying parent's widgets
        widgets.update({
            'land_title_document': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'legal_mortgage_agreement_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'power_of_attorney_document': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'supporting_documents': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out', 'rows': 3}),
            'no_existing_npl': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
        })

class SalaryBackedLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = SalaryBackedLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'salary_passing_union_ge_3_months', 'savings_ge_1_10_loan',
            'copy_of_effective_service_document',
            'irrevocable_salary_transfer_document',
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'salary_passing_union_ge_3_months': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'savings_ge_1_10_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'copy_of_effective_service_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'irrevocable_salary_transfer_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
        })
        labels = {
            'savings_ge_1_10_loan': 'Savings Balance is at least 1/10th of Loan Amount',
            'salary_passing_union_ge_3_months': 'Salary passing union greater than 3 months',
        }

class LoanWithinSavingsApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = LoanWithinSavingsApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'savings_covers_loan_plus_interest', 'loan_amount_blocked_in_savings', 'no_active_default'
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'savings_covers_loan_plus_interest': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'loan_amount_blocked_in_savings': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'no_active_default': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
        })

class DailySavingsLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = DailySavingsLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'daily_savings_active_ge_6_months', 'positive_loan_repayment_history',
            'savings_balance_ge_1_5_loan', 'signed_deduction_agreement_document',
            'valid_surety_bond_document'
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'daily_savings_active_ge_6_months': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'positive_loan_repayment_history': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'savings_balance_ge_1_5_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'signed_deduction_agreement_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'valid_surety_bond_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
        })
        labels = {
            'daily_savings_active_ge_6_months': 'Daily savings active greater than 6 months',
            'savings_balance_ge_1_5_loan': 'Savings balance greater than 1/5th of loan',
        }
class StandingOrderLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = StandingOrderLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'standing_order_active_ge_3_months', 'loan_duration_le_1_year',
            'savings_balance_ge_1_5_loan', 'no_existing_default_or_delinquency'
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'standing_order_active_ge_3_months': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'loan_duration_le_1_year': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'savings_balance_ge_1_5_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'no_existing_default_or_delinquency': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
        })
        labels = {
            'standing_order_active_ge_3_months': 'Standing Order active greater than 3 months',
            'loan_duration_le_1_year': 'Loan duration greater than 1 year',
            'savings_balance_ge_1_5_loan': 'Savings balance greater than 1/5th of loan',
        }

class RealEstateLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = RealEstateLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'loan_duration_ge_10_years',
            'loan_amount_le_10_percent_paid_up_capital',
            'land_title_in_borrowers_name',
            'valid_proof_of_source_of_income',
            'legal_mortgage_agreement_document_re', # Added from your model
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'loan_duration_ge_10_years': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'loan_amount_le_10_percent_paid_up_capital': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'land_title_in_borrowers_name': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'valid_proof_of_source_of_income': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'legal_mortgage_agreement_document_re': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
        })
        labels = {
            'loan_duration_ge_10_years': 'Loan duration greater than 10 year',
        }

class ContainerLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = ContainerLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'savings_balance_amount', 'savings_balance_ge_1_5_loan',
            'valid_proof_of_source_of_income',
            'bill_of_lading_document', 'custom_clearance_plan_document', # Added from your model
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'savings_balance_amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out', 'min': '0'}),
            'savings_balance_ge_1_5_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'valid_proof_of_source_of_income': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'bill_of_lading_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'custom_clearance_plan_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
        })
        labels = {
            'savings_balance_ge_1_5_loan':'Savings balance greater than 1/5th of loan',
        }

class AgriculturalLoanApplicationForm(BaseLoanApplicationForm):
    # Explicitly define loan_purpose_category with choices from model
    loan_purpose_category = forms.ChoiceField(
        choices=AGRICULTURAL_LOAN_PURPOSE_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out'}),
        label="Loan Purpose Category",
        required=False # Make it not required if it can be null in model
    )

    class Meta(BaseLoanApplicationForm.Meta):
        model = AgriculturalLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'is_land_personal_belonging', 'has_authorization_of_usage',
            'loan_purpose_category', # This field is now explicitly defined
            'savings_balance_amount',
            'savings_balance_ge_1_5_loan', 'valid_proof_of_source_of_income',
            'total_cost_estimate_document', # Added from your model
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'is_land_personal_belonging': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'has_authorization_of_usage': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'savings_balance_amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out', 'min': '0'}),
            'savings_balance_ge_1_5_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'valid_proof_of_source_of_income': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'total_cost_estimate_document': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
        })
        labels = {
            'savings_balance_ge_1_5_loan':'Savings balance greater than 1/5th of loan',
            'is_land_personal_belonging': 'Is the land a personal belonging?',
        }

class ExpressLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = ExpressLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'salary_deducted_at_source_or_standing_order', 'effective_service_available',
            'clearly_valid_purpose_of_loan', 'savings_balance_amount',
            'savings_balance_ge_1_10_loan', 'no_existing_delinquent_loan'
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'salary_deducted_at_source_or_standing_order': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'effective_service_available': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'clearly_valid_purpose_of_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'savings_balance_amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out', 'min': '0'}),
            'savings_balance_ge_1_10_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'no_existing_delinquent_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
        })
        # --- ADDED: Custom labels for ExpressLoanApplicationForm fields ---
        labels = {
            'savings_balance_ge_1_10_loan': 'Savings Balance is at least 1/10th of Loan Amount',
        }

    def clean(self):
        cleaned_data = super().clean()
        loan_term_years = cleaned_data.get('loan_term_years')

        if loan_term_years is not None:
            loan_term_months = loan_term_years * 12
            # Removed the express loan duration validation as requested
            # if loan_term_months > 3:
            #    self.add_error('loan_term_years', ValidationError(
            #        _('Express loan duration must not exceed 3 months.'),
            #        code='invalid_loan_term'
            #    ))
        return cleaned_data

# NEW: Business Loan Application Form
class BusinessLoanApplicationForm(BaseLoanApplicationForm):
    class Meta(BaseLoanApplicationForm.Meta):
        model = BusinessLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'valid_source_of_income_for_repayment', 'land_documents_attached',
            'savings_balance_ge_20_percent_loan', 'cost_estimate_provided'
        ]
        widgets = BaseLoanApplicationForm.Meta.widgets.copy()
        widgets.update({
            'valid_source_of_income_for_repayment': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'land_documents_attached': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'savings_balance_ge_20_percent_loan': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
            'cost_estimate_provided': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded'}),
        })
        labels = {
            'savings_balance_ge_20_percent_loan': 'Savings balance greater than 20% of loan',
        }


# NEW: User Registration Form
class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # Add email if you want it during registration
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out'}),
        }

# NEW: User Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out'})
    )
