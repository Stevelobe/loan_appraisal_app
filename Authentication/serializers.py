# users/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from credit_unions.serializers import CreditUnionSerializer
from credit_unions.models import CreditUnion, UserProfile
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),
        message="This username is already used"
        )]
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),
        message="This email is already used"
        )]
    )

    # A write-only field for password, so it's not included in read operations.
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    credit_union_id = serializers.PrimaryKeyRelatedField(
        queryset=CreditUnion.objects.all(),
        source='profile.credit_union', # Directs the data to the profile model's credit_union field
        write_only=True,
        required=False,
        allow_null=True # Matches the null=True on the model field
    )

    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'credit_union_id')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        credit_union_instance = profile_data.get('credit_union') # Get the CreditUnion instance or None

        # 2. Extract the CreditUnion object
        # You don't need the try/except block anymore, as DRF already validated the ID and fetched the object
        if credit_union_instance:
            credit_union = credit_union_instance
        else:
            credit_union = None # Allow None if required=False and allow_null=True
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            # is_staff=validated_data['is_staff'],
            # is_superuser=validated_data['is_superuser'],
            # is_active=validated_data.get('is_active', True)
        )
        UserProfile.objects.create(
            user=user,
            credit_union=credit_union # Assuming UserProfile has a ForeignKey called 'credit_union'
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username:
            raise serializers.ValidationError(
                {"username": "This field is required."}
            )

        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                pass # Let the default authentication handle invalid credentials
            else:
                attrs[self.username_field] = user.username
        
        
        try:
            data = super().validate(attrs)  
        except (AuthenticationFailed, serializers.ValidationError):
            raise serializers.ValidationError({
                "detail": "Bien vouloir verifier votre nom ou email et mot de passe."
            })
        data.update({
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # 'is_active': self.user.is_active,
            # 'is_staff': self.user.is_staff,
            # 'is_superuser': self.user.is_superuser
        })
        return data

# This serializer is used to return selected user information to the frontend.
class UserInfoSerializer(serializers.ModelSerializer):
    credit_union = serializers.SerializerMethodField()
    class Meta:
        model = User
        # Specify the fields you want to include in the user info response.
        # Ensure 'password' is NOT included here.
        fields = ('id', 'username', 'email', 'credit_union')

    def get_credit_union(self, user):
        """
        Retrieves the CreditUnion data via the user's profile and serializes it.
        """
        try:
            # Access the profile model (related_name='profile') and then the credit_union field
            cu = user.profile.credit_union
            if cu:
                # Use your CreditUnionSerializer to serialize the object
                return CreditUnionSerializer(cu).data
            return None
        except UserProfile.DoesNotExist:
            return None
