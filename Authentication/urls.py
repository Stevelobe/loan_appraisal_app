# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import RegisterView, LoginView, LogoutView, UserProfileView, UsersManagement, ActivateUserView # Import the new LoginView

# Define the URL patterns for the users app.
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('allusers/', UsersManagement.as_view(), name='users_management'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/', UserProfileView.as_view(), name='update-profile'),
    path('activate/<int:pk>/', ActivateUserView.as_view(), name='activate-user'),
]