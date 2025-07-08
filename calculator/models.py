# calculator/models.py

from django.db import models

class LoanApplication(models.Model):
    """
    Abstract base class for all loan applications to hold common fields.
    Specific loan types will inherit from this.
    """
    LOAN_TYPES = [
        ('mortgage', 'Mortgage Loan'),
        ('salary_backed', 'Salary-Backed Loan'),
        ('within_savings', 'Loan Within Savings'),
        ('above_savings', 'Loan Above Savings'),
        ('standing_order', 'Standing Order Loan'),
    ]

    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    annual_interest_rate_percent = models.DecimalField(max_digits=5, decimal_places=2)
    loan_term_years = models.IntegerField()
    borrower_gross_monthly_income = models.DecimalField(max_digits=15, decimal_places=2)
    existing_monthly_debt_payments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    submission_date = models.DateTimeField(auto_now_add=True)
    appraisal_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    approved = models.BooleanField(null=True, blank=True) # True/False/None (for board review)
    reasons = models.JSONField(default=list, blank=True) # Stores a list of reasons/criteria met/not met

    # --- NEW Fields for Approved Loans Report ---
    account_number = models.CharField(max_length=50, blank=True, null=True, help_text="Applicant's MFI Account Number")
    savings_balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text="Applicant's current savings balance at the MFI")

    # KYC Fields
    identity_card_number = models.CharField(max_length=50, blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    current_address = models.CharField(max_length=255, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    duration_with_mfi_years = models.IntegerField(blank=True, null=True)
    num_loans_other_mfi = models.IntegerField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)

    loan_purpose_document = models.FileField(upload_to='loan_purpose_docs/', blank=True, null=True)


    def __str__(self):
        return f"{self.applicant_name} - {self.get_loan_type_display()} - {self.loan_amount} XAF"

class MortgageLoanApplication(LoanApplication):
    legal_mortgage_agreement_document = models.FileField(upload_to='mortgage_docs/legal_agreements/', blank=True, null=True)
    land_title_document = models.FileField(upload_to='mortgage_docs/land_titles/', blank=True, null=True)
    power_of_attorney_document = models.FileField(upload_to='mortgage_docs/poa/', blank=True, null=True)
    supporting_documents = models.FileField(upload_to='mortgage_docs/supporting/', blank=True, null=True)
    no_existing_npl = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mortgage Loan Application"
        verbose_name_plural = "Mortgage Loan Applications"

    def __str__(self):
        return f"Mortgage: {self.applicant_name} - {self.loan_amount} XAF"

class SalaryBackedLoanApplication(LoanApplication):
    salary_passing_union_ge_3_months = models.BooleanField(default=False)
    copy_of_effective_service_document = models.FileField(upload_to='salary_docs/effective_service/', blank=True, null=True)
    irrevocable_salary_transfer_document = models.FileField(upload_to='salary_docs/transfer_docs/', blank=True, null=True)
    savings_ge_1_10_loan = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Salary-Backed Loan Application"
        verbose_name_plural = "Salary-Backed Loan Applications"

    def __str__(self):
        return f"Salary-Backed: {self.applicant_name} - {self.loan_amount} XAF"

class LoanWithinSavingsApplication(LoanApplication):
    savings_covers_loan_plus_interest = models.BooleanField(default=False)
    loan_amount_blocked_in_savings = models.BooleanField(default=False)
    no_active_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Loan Within Savings Application"
        verbose_name_plural = "Loan Within Savings Applications"

    def __str__(self):
        return f"Within Savings: {self.applicant_name} - {self.loan_amount} XAF"

class LoanAboveSavingsApplication(LoanApplication):
    daily_savings_active_ge_6_months = models.BooleanField(default=False)
    signed_deduction_agreement_document = models.FileField(upload_to='above_savings_docs/deduction_agreements/', blank=True, null=True)
    valid_surety_bond_document = models.FileField(upload_to='above_savings_docs/surety_bonds/', blank=True, null=True)
    positive_loan_repayment_history = models.BooleanField(default=False)
    savings_balance_ge_1_5_loan = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Loan Above Savings Application"
        verbose_name_plural = "Loan Above Savings Applications"

    def __str__(self):
        return f"Above Savings: {self.applicant_name} - {self.loan_amount} XAF"

class StandingOrderLoanApplication(LoanApplication):
    standing_order_active_ge_3_months = models.BooleanField(default=False)
    loan_duration_le_1_year = models.BooleanField(default=False)
    savings_balance_ge_1_5_loan = models.BooleanField(default=False)
    no_existing_default_or_delinquency = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Standing Order Loan Application"
        verbose_name_plural = "Standing Order Loan Applications"

    def __str__(self):
        return f"Standing Order: {self.applicant_name} - {self.loan_amount} XAF"