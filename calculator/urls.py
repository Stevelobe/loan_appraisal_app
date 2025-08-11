# calculator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --- Authentication URLs ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- Other Loan Application and Dashboard URLs ---
    path('', views.loan_selection_view, name='loan_selection'),
    # CORRECTED: Point to the view functions, not the model classes
    path('mortgage/', views.mortgage_loan_application, name='mortgage_loan_application'),
    path('salary-backed/', views.salary_backed_loan_application, name='salary_backed_loan_application'),
    path('loan-within-savings/', views.loan_within_savings_application, name='loan_within_savings_application'),
    path('daily-savings/', views.daily_savings_loan_application, name='daily_savings_loan_application'),
    path('standing-order/', views.standing_order_loan_application, name='standing_order_loan_application'),
    path('real-estate/', views.real_estate_loan_application, name='real_estate_loan_application'),
    path('container/', views.container_loan_application, name='container_loan_application'),
    path('agricultural/', views.agricultural_loan_application, name='agricultural_loan_application'),
    path('express/', views.express_loan_application, name='express_loan_application'),
    path('business/', views.business_loan_application, name='business_loan_application'),

    # Existing result/dashboard views
    path('appraisal-results/', views.appraisal_results_display_view, name='appraisal_results'),
    path('approved-loans/', views.approved_loans_list, name='approved_loans_list'),
    path('cobac-regulations/', views.cobac_regulations_and_5cs_view, name='cobac_regulations_and_5cs'),
    path('loan-review-dashboard/', views.loan_review_dashboard, name='loan_review_dashboard'),

    # URL for PDF download
    path('appraisal-results/download-pdf/<int:pk>/', views.download_appraisal_pdf, name='download_appraisal_pdf'),

    # --- NEW: URL for deleting approved loans ---
    path('approved-loans/delete/', views.delete_approved_loans, name='delete_approved_loans'),
]