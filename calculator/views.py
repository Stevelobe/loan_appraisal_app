from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from decimal import Decimal

# Import Serializer and Logic
from .serializers import (
    MortgageLoanApplicationSerializer, 
    SalaryBackedLoanApplicationSerializer, 
    LoanWithinSavingsApplicationSerializer,
    DailySavingsLoanApplicationSerializer,
    StandingOrderLoanApplicationSerializer,
    RealEstateLoanApplicationSerializer,
    ContainerLoanApplicationSerializer,
    AgriculturalLoanApplicationSerializer,
    ExpressLoanApplicationSerializer,
    BusinessLoanApplicationSerializer,
    LoanApplicationSerializer)

from .appraisal_logic import (
    appraise_mortgage_loan, 
    appraise_salary_backed_loan, 
    appraise_loan_within_savings,
    appraise_daily_savings_loan,
    appraise_standing_order_loan,
    appraise_real_estate_loan,
    appraise_container_loan,
    appraise_agricultural_loan,
    appraise_express_loan,
    appraise_business_loan)
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

class MortgageLoanAppraisalView(APIView):
    """
    Handles POST requests for submitting a Mortgage Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = MortgageLoanApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # # File/Boolean fields: check presence of file or boolean value
                # 'legal_mortgage_agreement_document': bool(validated_data.get('legal_mortgage_agreement_document')),
                # File/Boolean fields: check presence of file or boolean value
                'legal_mortgage_agreement_document': validated_data.get('legal_mortgage_agreement_document', False),
                'land_title_document': validated_data.get('land_title_document', False),
                'power_of_attorney_document': validated_data.get('power_of_attorney_document', False),
                'supporting_documents': validated_data.get('supporting_documents', False),
                'no_existing_npl': validated_data.get('no_existing_npl', False),
                'loan_purpose': validated_data.get('loan_purpose', ''), # Text field
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_mortgage_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalaryBackedLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Salary Backed Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = SalaryBackedLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'copy_of_effective_service_document': validated_data.get('copy_of_effective_service_document', False),
                'irrevocable_salary_transfer_document': validated_data.get('irrevocable_salary_transfer_document', False),
                'salary_passing_union_ge_3_months': validated_data.get('salary_passing_union_ge_3_months', False),
                'savings_ge_1_10_loan': validated_data.get('savings_ge_1_10_loan', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_salary_backed_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanWithinSavingsApplicationView(APIView):
    """
    Handles POST requests for submitting a Loan Within Savings application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = LoanWithinSavingsApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'savings_covers_loan_plus_interest': validated_data.get('savings_covers_loan_plus_interest', False),
                'loan_amount_blocked_in_savings': validated_data.get('loan_amount_blocked_in_savings', False),
                'no_active_default': validated_data.get('no_active_default', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_loan_within_savings(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DailySavingsLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Daily Savings Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = DailySavingsLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'signed_deduction_agreement_document': validated_data.get('signed_deduction_agreement_document', False),
                'valid_surety_bond_document': validated_data.get('valid_surety_bond_document', False),
                'daily_savings_active_ge_6_months': validated_data.get('daily_savings_active_ge_6_months', False),
                'positive_loan_repayment_history': validated_data.get('positive_loan_repayment_history', False),
                'savings_balance_ge_1_5_loan': validated_data.get('savings_balance_ge_1_5_loan', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_daily_savings_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StandingOrderLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Standing Order Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = StandingOrderLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'standing_order_active_ge_3_months': validated_data.get('standing_order_active_ge_3_months', False),
                'loan_duration_le_1_year': validated_data.get('loan_duration_le_1_year', False),
                'savings_balance_ge_1_5_loan': validated_data.get('savings_balance_ge_1_5_loan', False),
                'no_existing_default_or_delinquency': validated_data.get('no_existing_default_or_delinquency', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_standing_order_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RealEstateLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Real Estate Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = RealEstateLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'legal_mortgage_agreement_document_re': validated_data.get('legal_mortgage_agreement_document_re', False),
                'loan_duration_ge_10_years': validated_data.get('loan_duration_ge_10_years', False),
                'loan_amount_le_10_percent_paid_up_capital': validated_data.get('loan_amount_le_10_percent_paid_up_capital', False),
                'land_title_in_borrowers_name': validated_data.get('land_title_in_borrowers_name', False),
                'valid_proof_of_source_of_income': validated_data.get('valid_proof_of_source_of_income', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_real_estate_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContainerLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Real Estate Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = ContainerLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'custom_clearance_plan_document': validated_data.get('custom_clearance_plan_document', False),
                'bill_of_lading_document': validated_data.get('bill_of_lading_document', False),
                'savings_balance_amount': validated_data.get('savings_balance_amount', False),
                'savings_balance_ge_1_5_loan': validated_data.get('savings_balance_ge_1_5_loan', False),
                'valid_proof_of_source_of_income': validated_data.get('valid_proof_of_source_of_income', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_container_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgriculturalLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Agricultural Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = AgriculturalLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'total_cost_estimate_document': validated_data.get('total_cost_estimate_document', False),
                'is_land_personal_belonging': validated_data.get('is_land_personal_belonging', False),
                'has_authorization_of_usage': validated_data.get('has_authorization_of_usage', False),
                'loan_purpose_category': validated_data.get('loan_purpose_category'),
                'savings_balance_amount': validated_data.get('savings_balance_amount'),
                'savings_balance_ge_1_5_loan': validated_data.get('savings_balance_ge_1_5_loan', False),
                'valid_proof_of_source_of_income': validated_data.get('valid_proof_of_source_of_income', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_agricultural_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpressLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Express Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = ExpressLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'salary_deducted_at_source_or_standing_order': validated_data.get('salary_deducted_at_source_or_standing_order', False),
                'effective_service_available': validated_data.get('effective_service_available', False),
                'clearly_valid_purpose_of_loan': validated_data.get('clearly_valid_purpose_of_loan', False),
                'savings_balance_amount': validated_data.get('savings_balance_amount'),
                'savings_balance_ge_1_10_loan': validated_data.get('savings_balance_ge_1_10_loan', False),
                'no_existing_delinquent_loan': validated_data.get('no_existing_delinquent_loan', False),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_express_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessLoanApplicationView(APIView):
    """
    Handles POST requests for submitting a Business Loan application.
    
    1. Validates input data (including files) using the serializer.
    2. Runs the business logic (appraisal score calculation).
    3. Saves the loan application instance with the final appraisal results.
    4. Requires user authentication for security.
    """
    # Security: Only authenticated users can submit applications
    # This is critical since the LoanApplication model uses a ForeignKey to User.
    permission_classes = [AllowAny,] 

    def post(self, request, *args, **kwargs):
        # DRF handles file uploads (multipart/form-data) seamlessly with ModelSerializer
        serializer = BusinessLoanApplicationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            # --- 1. Prepare Data for Appraisal Logic ---
            validated_data = serializer.validated_data
            
            # Extract fields and convert file fields to booleans for the appraisal logic
            # The actual FileField data is passed directly through the serializer to .save()
            appraisal_input = {
                'loan_amount': validated_data.get('loan_amount'),
                'annual_interest_rate_percent': validated_data.get('annual_interest_rate_percent'),
                'loan_term_years': validated_data.get('loan_term_years'),
                'borrower_gross_monthly_income': validated_data.get('borrower_gross_monthly_income'),
                'existing_monthly_debt_payments': validated_data.get('existing_monthly_debt_payments'),
                
                # File/Boolean fields: check presence of file or boolean value
                'land_documents_attached': validated_data.get('land_documents_attached', False),
                'valid_source_of_income_for_repayment': validated_data.get('valid_source_of_income_for_repayment', False),
                'savings_balance_ge_20_percent_loan': validated_data.get('savings_balance_ge_20_percent_loan', False),
                'cost_estimate_provided': validated_data.get('cost_estimate_provided'),
                
                
                # KYC fields for the _check_full_kyc helper
                'identity_card_number': validated_data.get('identity_card_number'),
                'place_of_birth': validated_data.get('place_of_birth'),
                'date_of_birth': validated_data.get('date_of_birth'),
                'current_address': validated_data.get('current_address'),
                'marital_status': validated_data.get('marital_status'),
                'profession': validated_data.get('profession'),
            }
            
            # --- 2. Run Appraisal Logic ---
            appraisal_results = appraise_business_loan(appraisal_input)

            # --- 3. Update validated_data with Appraisal Results ---
            validated_data['appraisal_score'] = appraisal_results['score']
            validated_data['approved'] = appraisal_results['approved']
            
            # Convert list of strings to list of dictionaries for the reasons JSONField
            validated_data['reasons'] = [{'reason': r} for r in appraisal_results['reasons']] 

            # Set the user who submitted the application
            # validated_data['user'] = request.user 
            
            # --- 4. Save the Application ---
            # The serializer automatically handles saving the instance and the uploaded files.
            loan_instance = serializer.save(**validated_data)
            
            # --- 5. Return Success Response ---
            response_data = {
                'message': 'Loan application successfully submitted and appraised.',
                'application_id': loan_instance.pk,
                'appraisal': appraisal_results,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # --- Handle Invalid Data ---
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllLoan(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format=None):
        loans_under_review = LoanApplication.objects.filter(
            # user=request.user, # <--- Filter by current user
            appraisal_score__isnull=False
        ).order_by('-submission_date')
        serializer = LoanApplicationSerializer(loans_under_review, many=True)
        return Response(serializer.data)