# calculator/urls.py
from django.urls import path
from . import views # Import the views from your calculator app

urlpatterns = [
    path('', views.loan_appraisal_view, name='loan_appraisal_calculator'), # Maps root of app to loan_appraisal_view
]