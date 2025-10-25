from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserInfoSerializer, CustomTokenObtainPairSerializer
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView
# This view handles user registration.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# This custom LoginView handles authentication and sets JWT tokens as HTTP-only cookies.
class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = (AllowAny,) 

    def post(self, request, *args, **kwargs):
        # Create a response object.
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        return response
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    # Use the UserInfoSerializer to handle the data for the user profile.
    serializer_class = UserInfoSerializer
    
    # Override the get_object method to return the authenticated user's profile.
    # This ensures that a user can only modify their own data, not another user's.
    def get_object(self):
        return self.request.user

class UsersManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, format=None):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)   

class ActivateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request, pk,format=None):
        users = User.objects.get(pk=pk)
        users.is_active = not users.is_active
        users.save()
        return Response(status=status.HTTP_204_NO_CONTENT)   