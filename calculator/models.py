# calculator/models.py
from django.db import models

class LoanApplication(models.Model):
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    annual_interest_rate_percent = models.DecimalField(max_digits=5, decimal_places=2)
    loan_term_years = models.IntegerField()
    borrower_gross_monthly_income = models.DecimalField(max_digits=15, decimal_places=2)
    existing_monthly_debt_payments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit_score = models.CharField(max_length=50, blank=True, null=True) # e.g., "Good", "Average", "Poor"
    application_date = models.DateTimeField(auto_now_add=True)

    # Appraisal Results
    approved = models.BooleanField(default=False)
    reasons = models.JSONField(default=list) # Stores a list of strings
    monthly_payment_new_loan = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_monthly_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dti_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    loan_amount_to_annual_income_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"Loan Application for {self.loan_amount} - {'Approved' if self.approved else 'Declined'}"