from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny , SAFE_METHODS
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model

import k8s.k8s as k
User = get_user_model()

from asb.serializers import *

import os

class deploy(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        #comprueba si hay lab asignado al usuario
        #si hay caducado
            #se avisa
        #si no hay activo
            #se crea
        #si hay activo pero no levantado
            #se levanta
            #se marca en activo
        print('yay')
        k.deploy('lab-deployment.yaml')
        return HttpResponse( status=200)

class LabView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post (self, request, *args, **kwargs):
        print(request.auth.key)
        user = Token.objects.get(key=request.auth.key).user
        serializer = UserSerializer(data={'user':user.id})
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()   
            return HttpResponse(serializer.data, status=204)
        else:
            return HttpResponse(serializer.data, status=403)
            
    def get(self,request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)