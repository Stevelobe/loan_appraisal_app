# calculator/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import datetime
from django.contrib.auth.models import User # NEW: Import the User model

class LoanApplication(models.Model):
    """
    Base class for all loan applications to hold common fields.
    Specific loan types will inherit from this using multi-table inheritance.
    """
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

    # NEW FIELD: Link to the User model
    # This field will store which user submitted this loan application.
    # on_delete=models.CASCADE means if a user is deleted, their loans are also deleted.
    # related_name allows you to access a user's loans like user.loan_applications.all()
    # null=True, blank=True allows existing loans to not have a user initially (if you have old data)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications', null=True, blank=True)

    applicant_name = models.CharField(max_length=200, default="Default Applicant")
    applicant_email = models.EmailField(default="default@example.com")
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default='mortgage')
    
    loan_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('1000000.00'),
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    annual_interest_rate_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('10.00'),
        validators=[MinValueValidator(Decimal('6.00')), MaxValueValidator(Decimal('60.00'))]
    )
    loan_term_years = models.IntegerField(default=5, validators=[MinValueValidator(1)])
    borrower_gross_monthly_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('150000.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    existing_monthly_debt_payments = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    appraisal_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    approved = models.BooleanField(null=True, blank=True)
    reasons = models.JSONField(default=list, blank=True) # Stores list of reason dictionaries
    approver_comments = models.TextField(blank=True, null=True) # Added for approver comments

    # --- Fields for Approved Loans Report ---
    account_number = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        default='UNKNOWN',
        help_text="Applicant's MFI Account Number"
    )

    # --- NEW FIELDS: Date of Loan and Current Location ---
    date_of_loan = models.DateField(
        default=datetime.date.today,
        help_text="The date the loan application is being processed."
    )
    current_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Applicant's current geographical location."
    )

    # KYC Fields
    identity_card_number = models.CharField(max_length=50, blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    current_address = models.CharField(max_length=255, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    duration_with_mfi_years = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[MinValueValidator(0)]
    )
    num_loans_other_mfi = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[MinValueValidator(0)]
    )
    profession = models.CharField(max_length=100, blank=True, null=True)

    # Changed from FileField to TextField and renamed
    loan_purpose = models.TextField(blank=True, null=True, help_text="Describe the purpose of the loan.") 

    def __str__(self):
        return f"{self.applicant_name} - {self.get_loan_type_display()} - {self.loan_amount} XAF"

    def get_loan_type_display(self):
        type_map = dict(self.LOAN_TYPES)
        return type_map.get(self.loan_type, self.loan_type)

class MortgageLoanApplication(LoanApplication):
    legal_mortgage_agreement_document = models.FileField(upload_to='mortgage_docs/legal_agreements/', blank=True, null=True)
    land_title_document = models.BooleanField(default=False, help_text="Does the borrower have a Land Title in their name?")
    power_of_attorney_document = models.BooleanField(default=False, help_text="Is there a Power of Attorney (if applicable)?")
    supporting_documents = models.TextField(blank=True, null=True, help_text="List supporting documents like Site Plan, Quotes, etc.")
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

class DailySavingsLoanApplication(LoanApplication):
    daily_savings_active_ge_6_months = models.BooleanField(default=False)
    signed_deduction_agreement_document = models.FileField(upload_to='daily_savings_docs/deduction_agreements/', blank=True, null=True)
    valid_surety_bond_document = models.FileField(upload_to='daily_savings_docs/surety_bonds/', blank=True, null=True)
    positive_loan_repayment_history = models.BooleanField(default=False)
    savings_balance_ge_1_5_loan = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Daily Savings Loan Application"
        verbose_name_plural = "Daily Savings Loan Applications"

    def __str__(self):
        return f"Daily Savings: {self.applicant_name} - {self.loan_amount} XAF"

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

class RealEstateLoanApplication(LoanApplication):
    loan_duration_ge_10_years = models.BooleanField(
        default=False,
        help_text="Is the loan duration greater than or equal to 10 years?"
    )
    loan_amount_le_10_percent_paid_up_capital = models.BooleanField(
        default=False,
        help_text="Does the loan amount not exceed 10% of paid-up capital? (System Verified)"
    )
    legal_mortgage_agreement_document_re = models.FileField(
        upload_to='real_estate_docs/legal_agreements/',
        blank=True,
        null=True,
        help_text="Scanned copy of the signed Legal Mortgage Agreement."
    )
    land_title_in_borrowers_name = models.BooleanField(
        default=False,
        help_text="Is the Land Title in the borrower's name? (System Verified)"
    )
    valid_proof_of_source_of_income = models.BooleanField(
        default=False,
        help_text="Is there valid proof of source of income? (System Verified)"
    )

    class Meta:
        verbose_name = "Real Estate Loan Application"
        verbose_name_plural = "Real Estate Loan Applications"

    def __str__(self):
        return f"Real Estate: {self.applicant_name} - {self.loan_amount} XAF"

class ContainerLoanApplication(LoanApplication):
    bill_of_lading_document = models.FileField(
        upload_to='container_docs/bill_of_lading/',
        blank=True,
        null=True,
        help_text="Upload a copy of the Bill of Lading."
    )
    custom_clearance_plan_document = models.FileField(
        upload_to='container_docs/custom_clearance/',
        blank=True,
        null=True,
        help_text="Upload the Custom Clearance Plan."
    )
    savings_balance_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Current savings balance amount (XAF)."
    )
    savings_balance_ge_1_5_loan = models.BooleanField(
        default=False,
        help_text="Is savings balance 1/5 or more of the loan amount? (System Verified)"
    )
    valid_proof_of_source_of_income = models.BooleanField(
        default=False,
        help_text="Is there valid proof of source of income? (System Verified)"
    )

    class Meta:
        verbose_name = "Container Loan Application"
        verbose_name_plural = "Container Loan Applications"

    def __str__(self):
        return f"Container: {self.applicant_name} - {self.loan_amount} XAF"

class AgriculturalLoanApplication(LoanApplication):
    LOAN_PURPOSE_CHOICES = [
        ('crops', 'Crops (e.g., maize, cassava, cocoa)'),
        ('livestock', 'Livestock (e.g., cattle, poultry, pigs)'),
    ]

    is_land_personal_belonging = models.BooleanField(
        default=False,
        help_text="Is the land a personal belonging of the loan applicant?"
    )
    has_authorization_of_usage = models.BooleanField(
        default=False,
        help_text="If land is not personal, is there an authorization of usage?"
    )
    loan_purpose_category = models.CharField(
        max_length=50,
        choices=LOAN_PURPOSE_CHOICES,
        blank=True,
        null=True,
        help_text="Select the primary purpose of this agricultural loan."
    )
    savings_balance_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Current savings balance amount (XAF)."
    )
    savings_balance_ge_1_5_loan = models.BooleanField(
        default=False,
        help_text="Is savings balance 1/5 or more (20%) of the loan amount? (System Verified)"
    )
    total_cost_estimate_document = models.FileField(
        upload_to='agricultural_docs/cost_estimates/',
        blank=True,
        null=True,
        help_text="Upload the total cost estimate of products and inputs."
    )
    valid_proof_of_source_of_income = models.BooleanField(
        default=False,
        help_text="Is there valid proof of source of income? (System Verified)"
    )

    class Meta:
        verbose_name = "Agricultural Loan Application"
        verbose_name_plural = "Agricultural Loan Applications"

    def __str__(self):
        return f"Agricultural: {self.applicant_name} - {self.loan_amount} XAF"

class ExpressLoanApplication(LoanApplication):
    salary_deducted_at_source_or_standing_order = models.BooleanField(
        default=False,
        help_text="Is salary deducted at source or is a standing order available?"
    )
    effective_service_available = models.BooleanField(
        default=False,
        help_text="Is a copy of effective service available?"
    )
    clearly_valid_purpose_of_loan = models.BooleanField(
        default=False,
        help_text="Is there a clearly and valid purpose for the loan?"
    )
    savings_balance_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Current savings balance amount (XAF)."
    )
    savings_balance_ge_1_10_loan = models.BooleanField(
        default=False,
        help_text="Is savings balance 1/10 or more (10%) of the loan amount? (System Verified)"
    )
    no_existing_delinquent_loan = models.BooleanField(
        default=False,
        help_text="Is there no existing delinquent loan? (System Verified)"
    )

    class Meta:
        verbose_name = "Express Loan Application"
        verbose_name_plural = "Express Loan Applications"

    def __str__(self):
        return f"Express: {self.applicant_name} - {self.loan_amount} XAF"

# NEW: Business Loan Application Model
class BusinessLoanApplication(LoanApplication):
    valid_source_of_income_for_repayment = models.BooleanField(
        default=False,
        help_text="A valid source of income for repayment is highly needed."
    )
    land_documents_attached = models.FileField(
        upload_to='business_docs/land_documents/',
        blank=True,
        null=True,
        help_text="Copies of land documents attached."
    )
    savings_balance_ge_20_percent_loan = models.BooleanField(
        default=False,
        help_text="Savings balance must be at least 20% of loan amount."
    )
    cost_estimate_provided = models.BooleanField(
        default=False,
        help_text="The cost estimate of the things to purchase provided."
    )

    class Meta:
        verbose_name = "Business Loan Application"
        verbose_name_plural = "Business Loan Applications"

    def __str__(self):
        return f"Business: {self.applicant_name} - {self.loan_amount} XAF"
