from django.urls import path
from .views import CreditUnionAPIView, CreditAPIView

urlpatterns = [
    path('add/', CreditUnionAPIView.as_view(), name='credit-union'),
    path('view/', CreditAPIView.as_view(), name='relation')
]   