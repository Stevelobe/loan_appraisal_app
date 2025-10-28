from rest_framework import serializers
from .models import CreditUnion, UserProfile

class CreditUnionSerializer(serializers.ModelSerializer):
    """
    Serializer for the CreditUnion model.
    Handles converting CreditUnion objects to JSON format for the API.
    """
    class Meta:
        # The model that this serializer is based on
        model = CreditUnion
        # The fields to be included in the serialized output.
        # 'id' is Django's auto-generated Primary Key (CreditUnionID).
        fields = [
            'id', 
            'name', 
            'address', 
            'contact_email', 
        ]

class UserCreditSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserProfile
        fields = [
            
            'user',
            'credit_union',
        ]