# calculator/forms.py

from django import forms
from .models import (
    LoanApplication, MortgageLoanApplication, SalaryBackedLoanApplication,
    LoanWithinSavingsApplication, LoanAboveSavingsApplication, StandingOrderLoanApplication
)
from decimal import Decimal

# Define common CSS classes
INPUT_CLASSES = 'block w-full px-4 py-2.5 text-base text-slate-800 bg-white border border-slate-300 rounded-xl shadow-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ease-in-out'
CHECKBOX_CLASSES = 'form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500 border-gray-300'
FILE_INPUT_CLASSES = 'block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-all duration-200 ease-in-out cursor-pointer'

class LoanTypeSelectionForm(forms.Form):
    loan_type = forms.ChoiceField(
        label="Select Loan Type",
        choices=LoanApplication.LOAN_TYPES,
        widget=forms.Select(attrs={'class': INPUT_CLASSES})
    )

class BaseLoanApplicationForm(forms.ModelForm):
    applicant_name = forms.CharField(
        label="Applicant's Full Name",
        max_length=200,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., John Doe'})
    )
    applicant_email = forms.EmailField(
        label="Applicant's Email",
        widget=forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., john.doe@example.com'})
    )
    loan_amount = forms.DecimalField(
        label="Loan Amount (XAF)",
        min_value=Decimal('100000'),
        max_value=Decimal('1000000000'),
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 5,000,000'})
    )
    annual_interest_rate_percent = forms.DecimalField(
        label="Annual Interest Rate (%)",
        min_value=Decimal('1.0'),
        max_value=Decimal('30.0'),
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 12.5'})
    )
    loan_term_years = forms.IntegerField(
        label="Loan Term (Years)",
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 5'})
    )
    borrower_gross_monthly_income = forms.DecimalField(
        label="Borrower's Gross Monthly Income (XAF)",
        min_value=Decimal('10000'),
        max_value=Decimal('10000000'),
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 700,000'})
    )
    existing_monthly_debt_payments = forms.DecimalField(
        label="Existing Monthly Debt Payments (XAF)",
        min_value=Decimal('0'),
        max_value=Decimal('5000000'),
        initial=Decimal('0'),
        required=False,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 50,000'})
    )

    # --- NEW Fields for Approved Loans Report ---
    account_number = forms.CharField(
        label="MFI Account Number",
        max_length=50,
        required=False, # Set to True for mandatory input
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., MFI-123456'})
    )
    savings_balance = forms.DecimalField(
        label="Current Savings Balance (XAF)",
        min_value=Decimal('0'),
        max_value=Decimal('1000000000'),
        required=False, # Set to True for mandatory input
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 1,500,000'})
    )

    # KYC Fields
    identity_card_number = forms.CharField(
        label="Identity Card Number",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 1234567890'})
    )
    place_of_birth = forms.CharField(
        label="Place of Birth",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., Yaounde'})
    )
    current_address = forms.CharField(
        label="Current Address",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., Quartier Essos, Street 123'})
    )
    MARITAL_STATUS_CHOICES = [
        ('', 'Select Status'),
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=MARITAL_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': INPUT_CLASSES})
    )
    duration_with_mfi_years = forms.IntegerField(
        label="Duration with MFI (Years)",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 2'})
    )
    num_loans_other_mfi = forms.IntegerField(
        label="Number of Loans in Other MFIs",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 0'})
    )
    profession = forms.CharField(
        label="Profession",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., Software Engineer'})
    )

    loan_purpose_document = forms.FileField(
        label="Purpose of Loan Document (e.g., Explaining Use of Funds)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )

    class Meta:
        model = LoanApplication # BaseLoanApplicationForm is for LoanApplication model
        fields = [
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'savings_balance', # <--- NEW FIELDS HERE
            'identity_card_number', 'place_of_birth', 'current_address', 'marital_status',
            'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'loan_purpose_document'
        ]

# --- Specific Loan Application Forms (Meta fields updated) ---

class MortgageLoanApplicationForm(BaseLoanApplicationForm):
    legal_mortgage_agreement_document = forms.FileField(
        label="Legal Mortgage Agreement on Land Title",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )
    land_title_document = forms.FileField(
        label="Land Title in Borrower's Name",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )
    power_of_attorney_document = forms.FileField(
        label="Power of Attorney (if applicable)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )
    supporting_documents = forms.FileField(
        label="Supporting Documents (Site Plan, Quotes, etc.)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )
    no_existing_npl = forms.BooleanField(
        label="No Existing Non-Performing Loan (System Check)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )

    class Meta(BaseLoanApplicationForm.Meta):
        model = MortgageLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'legal_mortgage_agreement_document', 'land_title_document',
            'power_of_attorney_document', 'supporting_documents', 'no_existing_npl'
        ]

class SalaryBackedLoanApplicationForm(BaseLoanApplicationForm):
    salary_passing_union_ge_3_months = forms.BooleanField(
        label="Salary Passing Through Union for ≥ 3 Months (System Verified)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    savings_ge_1_10_loan = forms.BooleanField(
        label="Savings ≥ 1/10 of Loan Requested (System Verified)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    copy_of_effective_service_document = forms.FileField(
        label="Copy of Effective Service",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )
    irrevocable_salary_transfer_document = forms.FileField(
        label="Irrevocable Salary Transfer Document",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )

    class Meta(BaseLoanApplicationForm.Meta):
        model = SalaryBackedLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'salary_passing_union_ge_3_months', 'copy_of_effective_service_document',
            'irrevocable_salary_transfer_document', 'savings_ge_1_10_loan',
        ]

class LoanWithinSavingsApplicationForm(BaseLoanApplicationForm):
    savings_covers_loan_plus_interest = forms.BooleanField(
        label="Savings Covers Loan + Interest for Entire Tenure (System Confirmed)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    loan_amount_blocked_in_savings = forms.BooleanField(
        label="Loan Amount Is Blocked in Savings Account (System Confirmed)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    no_active_default = forms.BooleanField(
        label="No Active Default/Delinquent Loan (System Check)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )

    class Meta(BaseLoanApplicationForm.Meta):
        model = LoanWithinSavingsApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'savings_covers_loan_plus_interest', 'loan_amount_blocked_in_savings',
            'no_active_default'
        ]

class LoanAboveSavingsApplicationForm(BaseLoanApplicationForm):
    daily_savings_active_ge_6_months = forms.BooleanField(
        label="Daily Savings Active for at Least 6 Months (System Verified)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    positive_loan_repayment_history = forms.BooleanField(
        label="Positive Loan Repayment History (System Check)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    savings_balance_ge_1_5_loan = forms.BooleanField(
        label="Savings Balance ≥ 1/5 of Loan Requested (System Verified)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    signed_deduction_agreement_document = forms.FileField(
        label="Signed Deduction Agreement from Daily Savings",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )
    valid_surety_bond_document = forms.FileField(
        label="Signed Surety Bond (Valid Surety)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASSES})
    )

    class Meta(BaseLoanApplicationForm.Meta):
        model = LoanAboveSavingsApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'daily_savings_active_ge_6_months', 'signed_deduction_agreement_document',
            'valid_surety_bond_document', 'positive_loan_repayment_history',
            'savings_balance_ge_1_5_loan',
        ]

class StandingOrderLoanApplicationForm(BaseLoanApplicationForm):
    standing_order_active_ge_3_months = forms.BooleanField(
        label="Standing Order Active for ≥ 3 Months (System Verified)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    loan_duration_le_1_year = forms.BooleanField(
        label="Loan Duration ≤ 1 Year (Policy Restriction - System Check)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    savings_balance_ge_1_5_loan = forms.BooleanField(
        label="Savings Balance ≥ 1/5 of Loan Amount (System Verified)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )
    no_existing_default_or_delinquency = forms.BooleanField(
        label="No Existing Default or Delinquency (System Check)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES})
    )

    class Meta(BaseLoanApplicationForm.Meta):
        model = StandingOrderLoanApplication
        fields = BaseLoanApplicationForm.Meta.fields + [
            'standing_order_active_ge_3_months', 'loan_duration_le_1_year',
            'savings_balance_ge_1_5_loan', 'no_existing_default_or_delinquency'
        ]