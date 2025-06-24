# calculator/forms.py
from django import forms

class LoanApplicationForm(forms.Form):
    # Define a common class string for consistent, quality input styling
    INPUT_CLASSES = 'block w-full px-4 py-2.5 text-base text-slate-800 bg-white border border-slate-300 rounded-xl shadow-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ease-in-out'

    loan_amount = forms.DecimalField(
        label="Loan Amount (XAF)",
        min_value=100000,
        max_value=1000000000,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 5,000,000'})
    )
    annual_interest_rate_percent = forms.DecimalField(
        label="Annual Interest Rate (%)",
        min_value=1.0,
        max_value=30.0,
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
        min_value=10000,
        max_value=10000000,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 700,000'})
    )
    existing_monthly_debt_payments = forms.DecimalField(
        label="Existing Monthly Debt Payments (XAF)",
        min_value=0,
        max_value=5000000,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., 50,000'})
    )