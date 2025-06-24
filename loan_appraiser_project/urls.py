# loan_appraiser_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Django's built-in admin site
    path('calculator/', include('calculator.urls')), # Include URLs from your 'calculator' app
    path('', include('calculator.urls')), # OPTIONAL: Make the calculator the default page
]