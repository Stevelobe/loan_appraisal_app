from django.contrib import admin
from .models import LoanApplication, MortgageLoanApplication 
# Assuming your models are in a file named models.py in the same app directory

## -------------------------------------------------------------
## Custom Admin Class for LoanApplication
## -------------------------------------------------------------
class LoanApplicationAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin site
    list_display = ('applicant_name', 'loan_type', 'loan_amount', 'submission_date', 'approved')
    
    # Fields to use as links to the detail view
    list_display_links = ('applicant_name', 'loan_amount')
    
    # Fields to allow filtering in the right sidebar
    list_filter = ('loan_type', 'approved', 'submission_date')
    
    # Fields to allow searching
    search_fields = ('applicant_name', 'applicant_email', 'account_number', 'identity_card_number')
    
    # Organize fields into fieldsets for the detail view
    fieldsets = (
        ('Applicant Information', {
            'fields': ('user', 'applicant_name', 'applicant_email', 'account_number', 'current_location')
        }),
        ('Loan Details', {
            'fields': ('loan_type', 'loan_amount', 'annual_interest_rate_percent', 'loan_term_years', 'loan_purpose', 'date_of_loan'),
        }),
        ('Financial/KYC Information', {
            'fields': ('borrower_gross_monthly_income', 'existing_monthly_debt_payments', 
                       'identity_card_number', 'place_of_birth', 'date_of_birth', 
                       'current_address', 'marital_status', 'profession',
                       'duration_with_mfi_years', 'num_loans_other_mfi'),
        }),
        ('Processing & Approval', {
            'fields': ('appraisal_score', 'approved', 'reasons', 'approver_comments', 'submission_date'),
            'classes': ('collapse',), # You can collapse this section
        }),
    )
    
    # Make 'submission_date' read-only
    readonly_fields = ('submission_date',)

## -------------------------------------------------------------
## Custom Admin Class for MortgageLoanApplication
## -------------------------------------------------------------
class MortgageLoanApplicationAdmin(admin.ModelAdmin):
    # Inherits from LoanApplication, so it might have many common fields.
    # Customizing the display for Mortgage-specific fields
    list_display = ('applicant_name', 'loan_amount', 'land_title_document', 'no_existing_npl', 'approved')
    list_filter = ('land_title_document', 'no_existing_npl', 'approved')
    search_fields = ('applicant_name', 'account_number')
    
    # You can customize the fieldsets further if needed. 
    # For multi-table inheritance models, it's often best to display all relevant fields.
    fieldsets = (
        ('Mortgage-Specific Documents', {
            'fields': ('legal_mortgage_agreement_document', 'land_title_document', 'power_of_attorney_document', 'supporting_documents', 'no_existing_npl')
        }),
    )
    # Since MortgageLoanApplication inherits from LoanApplication, 
    # consider using `inlines` if you want to see all fields from the parent model 
    # on the child's admin page, or simply add all parent fields to the fieldsets.
    # A simpler approach for the child model (due to multi-table inheritance)
    # is often to register it as a regular model and include the inherited fields.
    
    # For brevity, let's keep it simple and register it.

## -------------------------------------------------------------
## Registration
## -------------------------------------------------------------
admin.site.register(LoanApplication, LoanApplicationAdmin)
admin.site.register(MortgageLoanApplication, MortgageLoanApplicationAdmin)