from rest_framework import serializers
from .models import( LoanApplication, 
MortgageLoanApplication, 
SalaryBackedLoanApplication, 
LoanWithinSavingsApplication, 
DailySavingsLoanApplication,
StandingOrderLoanApplication,
RealEstateLoanApplication,
ContainerLoanApplication,
AgriculturalLoanApplication,
ExpressLoanApplication,
BusinessLoanApplication,)
from decimal import Decimal

# Helper serializer for common fields if needed, but ModelSerializer is cleaner here

class MortgageLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Mortgage Loan Applications.
    
    The serializer explicitly sets the loan_type field upon creation 
    and validates all common and mortgage-specific fields.
    """
    # Override loan_amount and other Decimal fields to ensure they handle numeric input correctly
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )
    
    # We must explicitly define FileFields as they are often handled differently 
    # in ModelSerializer when inheriting from a parent model.
    legal_mortgage_agreement_document = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = MortgageLoanApplication
        # List all fields from both the base LoanApplication and the MortgageLoanApplication
        fields = [
            # Base Fields (Step 1 & 2)
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Mortgage Specific Fields (Step 3)
            'legal_mortgage_agreement_document', 'land_title_document', 
            'power_of_attorney_document', 'supporting_documents', 'no_existing_npl',
            
            # Read-only fields for output (or hidden input on client side)
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'mortgage'
        user = self.context['request'].user
        # When saving, the MortgageLoanApplication inherits from LoanApplication 
        # via multi-table inheritance, so we create the child instance directly.
        return MortgageLoanApplication.objects.create(user=user, **validated_data)

class SalaryBackedLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Salary-Backed Loan Applications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    # File fields made optional
    copy_of_effective_service_document = serializers.BooleanField(required=False, allow_null=True)
    irrevocable_salary_transfer_document = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = SalaryBackedLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Salary-Backed Specific Fields
            'salary_passing_union_ge_3_months', 'copy_of_effective_service_document', 
            'irrevocable_salary_transfer_document', 'savings_ge_1_10_loan',
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'salary_backed'
        user = self.context['request'].user
        return SalaryBackedLoanApplication.objects.create(user=user, **validated_data)

class LoanWithinSavingsApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Loan Within Savings Applications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = LoanWithinSavingsApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Salary-Backed Specific Fields
            'savings_covers_loan_plus_interest', 'loan_amount_blocked_in_savings', 
            'no_active_default',
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'within_savings'
        user = self.context['request'].user
        return LoanWithinSavingsApplication.objects.create(user=user, **validated_data)

class DailySavingsLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Daily Savings Loan Applications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = DailySavingsLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Salary-Backed Specific Fields
            'daily_savings_active_ge_6_months', 'signed_deduction_agreement_document', 
            'valid_surety_bond_document','positive_loan_repayment_history','savings_balance_ge_1_5_loan'
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'daily_savings'
        user = self.context['request'].user
        return DailySavingsLoanApplication.objects.create(user=user, **validated_data)

class StandingOrderLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Daily Savings Loan Applications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = StandingOrderLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Salary-Backed Specific Fields
            'standing_order_active_ge_3_months', 'loan_duration_le_1_year', 
            'savings_balance_ge_1_5_loan','no_existing_default_or_delinquency'
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'standing_order'
        user = self.context['request'].user
        return StandingOrderLoanApplication.objects.create(user=user, **validated_data)

class RealEstateLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Daily Savings Loan Applications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = RealEstateLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Salary-Backed Specific Fields
            'loan_duration_ge_10_years', 'loan_amount_le_10_percent_paid_up_capital', 
            'legal_mortgage_agreement_document_re','land_title_in_borrowers_name', 'valid_proof_of_source_of_income'
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'real_estate'
        user = self.context['request'].user
        return RealEstateLoanApplication.objects.create(user=user, **validated_data)

class ContainerLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Container Loan Applications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = ContainerLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Salary-Backed Specific Fields
            'bill_of_lading_document', 'custom_clearance_plan_document', 
            'savings_balance_amount','savings_balance_ge_1_5_loan', 'valid_proof_of_source_of_income'
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'container'
        user = self.context['request'].user
        return ContainerLoanApplication.objects.create(user=user, **validated_data)

class AgriculturalLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Agricultural LoanApplications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = AgriculturalLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Salary-Backed Specific Fields
            'is_land_personal_belonging', 'has_authorization_of_usage', 'total_cost_estimate_document',
            'loan_purpose_category','savings_balance_amount', 'savings_balance_ge_1_5_loan','valid_proof_of_source_of_income'
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'agricultural'
        user = self.context['request'].user
        return AgriculturalLoanApplication.objects.create(user=user, **validated_data)

class ExpressLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Express Loan LoanApplications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = ExpressLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Express Specific Fields
            'salary_deducted_at_source_or_standing_order', 'effective_service_available', 'clearly_valid_purpose_of_loan',
            'savings_balance_amount','savings_balance_ge_1_10_loan', 'no_existing_delinquent_loan'
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'express'
        user = self.context['request'].user
        return ExpressLoanApplication.objects.create(user=user, **validated_data)

class BusinessLoanApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data validation and creation for Business Loan LoanApplications.
    """
    loan_amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )

    class Meta:
        model = BusinessLoanApplication
        fields = [
            # Base Fields
            'applicant_name', 'applicant_email', 'loan_amount', 'annual_interest_rate_percent',
            'loan_term_years', 'borrower_gross_monthly_income', 'existing_monthly_debt_payments',
            'account_number', 'date_of_loan', 'loan_purpose', 
            
            # KYC Fields
            'identity_card_number', 'place_of_birth', 'date_of_birth', 'current_address', 
            'marital_status', 'duration_with_mfi_years', 'num_loans_other_mfi', 'profession',
            'current_location',
            
            # Business Specific Fields
            'valid_source_of_income_for_repayment', 'land_documents_attached', 'savings_balance_ge_20_percent_loan',
            'cost_estimate_provided'
            
            # Read-only fields
            'id', 'submission_date', 'loan_type', 'user'
        ]
        read_only_fields = ['id', 'submission_date', 'loan_type', 'user']

    def create(self, validated_data):
        """
        Set the loan_type explicitly before saving the instance.
        """
        validated_data['loan_type'] = 'business'
        user = self.context['request'].user
        return BusinessLoanApplication.objects.create(user=user, **validated_data)

class LoanApplicationSerializer(serializers.ModelSerializer):
    # Optional: If you want to display the human-readable loan type instead of the code
    loan_type_display = serializers.CharField(source='get_loan_type_display', read_only=True)

    class Meta:
        model = LoanApplication
        fields = [
            'id', # Always include 'id' for primary key
            'user', 
            'applicant_name',
            'applicant_email',
            'credit_union',
            'loan_type',
            'loan_type_display', # Include the optional display field
            'loan_amount',
            'annual_interest_rate_percent',
            'loan_term_years',
            'borrower_gross_monthly_income',
            'existing_monthly_debt_payments',
            'submission_date',
            'appraisal_score',
            'approved',
            'reasons',
            'approver_comments',
            'account_number',
            'date_of_loan',
            'current_location',
            'identity_card_number',
            'place_of_birth',
            'date_of_birth',
            'current_address',
            'marital_status',
            'duration_with_mfi_years',
            'num_loans_other_mfi',
            'profession',
            'loan_purpose',
        ]
        # Or, you can use __all__ if you prefer to include every field:
        # fields = '__all__'
        
        # Optional: Make fields read-only if they should only be set by the system
        read_only_fields = ('submission_date','user') 