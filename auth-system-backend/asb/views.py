from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny , SAFE_METHODS
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()

from asb.serializers import *
from asb.models import Invitation

from urllib.parse import urlparse
from urllib.parse import parse_qs

class UserCreate(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    #serializer_class = UserSerializer
    def post (self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()   
            return JsonResponse(data=serializer.data, status=204)
        else:
            return JsonResponse(data=serializer.data, status=403)
            
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
            return Response({'Message': 'Invalid Username and Password'}, status=401)

class getUserFromToken(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
            user = Token.objects.get(key=request.auth.key).user
            return JsonResponse(data={  'fname':user.first_name,
                                        'lname':user.last_name,
                                        'email':user.email}, status=200)
        

class invitationView(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = Token.objects.get(key=request.auth.key).user
        try:
            guest = CustomUser.objects.get(email=request.data.get('guest'))
        except:
            return JsonResponse(data={'error':'invalid guest'}, status=404)
        try:
            invitation = Invitation.add_relationship(user,guest)
        except Exception as e:
            print(e)
        return JsonResponse(data={}, status=200)

    def get(self,request):
        user = Token.objects.get(key=request.auth.key).user
        outcoming = Invitation.get_invited(user)
        o_l = []
        incoming = Invitation.get_invitations(user)
        i_l = []
        for o in outcoming :
            o_l.append({'email':o.from_person.__str__(),
                        'delete':False})
        for i in incoming :
            i_l.append({'email':i.to_person.__str__(),
                        'delete':False})
        return JsonResponse(data={
                                   'outcoming':list(o_l),
                                   'incoming':list(i_l),
                                   }, status=200)

class outcomingDelete(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    def delete(self,request,email):
        user = Token.objects.get(key=request.auth.key).user
        try:
            guest = CustomUser.objects.get(email=email)
            Invitation.remove_relationship(user,guest)
            return JsonResponse(data={'removed_invite_to':email}, status=200)
        except Exception as e:
            return JsonResponse(data={'error':e.__str__(),
                                        'guest':email}, status=500)
                                        
class incomingDelete(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    def delete(self,request,email):
        user = Token.objects.get(key=request.auth.key).user
        try:
            host = CustomUser.objects.get(email=email)
            Invitation.remove_relationship(host,user)
            return JsonResponse(data={'removed_invite_from':email}, status=200)
        except Exception as e:
            return JsonResponse(data={'error':e.__str__(),
                                        'host':email}, status=500)
 