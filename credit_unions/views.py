from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CreditUnion, UserProfile
from .serializers import CreditUnionSerializer,UserCreditSerializer
from django.http import Http404
class CreditUnionAPIView(APIView):
    def get_permissions(self):

        if self.request.method == 'POST':
            return [AllowAny()]
        return [AllowAny()]

    def get(self, request, format=None):
        credit = CreditUnion.objects.all()
        serializer = CreditUnionSerializer(credit, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CreditUnionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreditAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        relationuc = UserProfile.objects.all()
        serializer = UserCreditSerializer(relationuc, many=True)
        return Response(serializer.data)