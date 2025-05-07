from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny , SAFE_METHODS

from knox.auth import TokenAuthentication

from django.contrib.auth import get_user_model
User = get_user_model()

from asb.serializers import *

class UserCreate(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    #serializer_class = UserSerializer
    def post (self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()   
            return HttpResponse(serializer.data, status=204)
        else:
            return HttpResponse(serializer.data, status=403)

class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': [token.key], "Sucsses":"Login SucssesFully"}, status=status.HTTP_201_CREATED )
            return Response({'Massage': 'Invalid Username and Password'}, status=401)
