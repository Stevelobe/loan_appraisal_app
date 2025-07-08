# calculator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.loan_type_selection_view, name='loan_type_selection'),
    path('mortgage/', views.mortgage_loan_application_view, name='mortgage_loan_application'),
    path('salary-backed/', views.salary_backed_loan_application_view, name='salary_backed_loan_application'),
    path('within-savings/', views.loan_within_savings_application_view, name='loan_within_savings_application'),
    path('above-savings/', views.loan_above_savings_application_view, name='loan_above_savings_application'),
    path('standing-order/', views.standing_order_loan_application_view, name='standing_order_loan_application'),
    path('results/', views.appraisal_results_view, name='appraisal_results'),

    path('approved-loans/', views.approved_loans_list_view, name='approved_loans_list'),
    path('approved-loans/export/csv/', views.export_approved_loans_csv, name='export_approved_loans_csv'),
    # --- NEW URL for Deletion ---
    path('approved-loans/delete/', views.delete_approved_loans, name='delete_approved_loans'),
    path('cobac-and-5cs/', views.cobac_regulations_and_5cs_view, name='cobac_regulations_and_5cs'),
]