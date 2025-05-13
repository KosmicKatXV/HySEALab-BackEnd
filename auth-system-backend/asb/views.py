from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny , SAFE_METHODS
from rest_framework.authentication import TokenAuthentication

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
            
    def get(self,request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)

class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': [token.key], "Sucsess":"Login SucssesFully"}, status=status.HTTP_201_CREATED )
            return Response({'Massage': 'Invalid Username and Password'}, status=401)