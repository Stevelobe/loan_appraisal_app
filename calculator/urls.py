from django.urls import path
from .views import (
    MortgageLoanAppraisalView, 
    SalaryBackedLoanApplicationView, 
    LoanWithinSavingsApplicationView,
    DailySavingsLoanApplicationView,
    StandingOrderLoanApplicationView,
    RealEstateLoanApplicationView,
    ContainerLoanApplicationView,
    AgriculturalLoanApplicationView,
    ExpressLoanApplicationView,
    BusinessLoanApplicationView,
    AllLoan)

# The app_name is used for namespacing URLs (e.g., reverse('calculator:submit_mortgage'))
app_name = 'calculator'

urlpatterns = [
    # Maps to the desired API endpoint: /api/loan-appraisal/submit/mortgage/
    path(
        'submit/mortgage/', 
        MortgageLoanAppraisalView.as_view(), 
        name='submit_mortgage_loan'
    ),
    path(
        'submit/salary-backed/', 
        SalaryBackedLoanApplicationView.as_view(), 
        name='submit_salary_backed_loan'
    ),
    path(
        'submit/within-savings/', 
        LoanWithinSavingsApplicationView.as_view(), 
        name='submit_within_savings_loan'
    ),
    path(
        'submit/daily-savings/', 
        DailySavingsLoanApplicationView.as_view(), 
        name='submit_daily_savings_loan'
    ),
     path(
        'submit/standing-order-savings/', 
        StandingOrderLoanApplicationView.as_view(), 
        name='submit_standing_order_savings_loan'
    ),
     path(
        'submit/real-estate-savings/', 
        RealEstateLoanApplicationView.as_view(), 
        name='submit_real_estate_loan'
    ),
     path(
        'submit/container-savings/', 
        ContainerLoanApplicationView.as_view(), 
        name='submit_container_loan'
    ),
     path(
        'submit/agriculural-loan/', 
        AgriculturalLoanApplicationView.as_view(), 
        name='submit_agricultural_loan'
    ),
     path(
        'submit/express-savings/', 
        ExpressLoanApplicationView.as_view(), 
        name='submit_express_savings_loan'
    ),
     path(
        'submit/business-savings/', 
        BusinessLoanApplicationView.as_view(), 
        name='submit_business_savings_loan'
    ),
    path(
        'all-loan/',
        AllLoan.as_view(),
        name='all-loans'
    )
]
