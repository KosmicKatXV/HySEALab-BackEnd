from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny , SAFE_METHODS
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model

import k8s.k8s as k
from k8s.models import Lab
User = get_user_model()

from asb.serializers import *

import os

class deploymentView(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = Token.objects.get(key=request.auth.key).user
        lab = Lab(user=request.user)
        serializer = UserSerializer(data={'user':user.id})
        #comprueba si hay lab asignado al usuario
        print(lab)
        if lab is None:
            return JsonResponse(data={'error':'No Lanb assigned to this user'}, status=404)
        elif not k.getLabStatus(lab).get('ready'):
            print(k.getLabStatus(lab).get('ready'))
            #si lo hay se comprueba que no esté levantado:
            env = {'LAB_ID':Lab(user=request.user).__str__()}
            lab_yml = k.deploy('lab-deployment.yaml',env)
            return JsonResponse(data={'info':'A lab has been deployed.'}, status=200)
        else:
            print(k.getLabStatus(lab).get('ready'))
            return JsonResponse(data={'warning':'A lab has already been deployed. No action has been taken'}, status=200)
    def get(self,request):
        user = Token.objects.get(key=request.auth.key).user
        lab = Lab(user=request.user)
        try:
            return JsonResponse(data=k.getLab(lab), status=200)
        except:
            return JsonResponse(data={'error':'no lab has been found'}, status=404)
    
    def delete(self,request):
        return JsonResponse(status=404)

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