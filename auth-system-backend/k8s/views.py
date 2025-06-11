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

from asb.models  import Invitation
import k8s.k8s as k
User = get_user_model()

from asb.serializers import *
import os

class deploymentView(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = Token.objects.get(key=request.auth.key).user
        email = user.__str__()
        id = str(user.id)
        invitation_list = []
        for i in Invitation.get_invited(user):
            invitation_list.append({'email':i.from_person.__str__(),
                                    'id':str(i.from_person.id)})
        #comprueba si hay lab asignado al usuario
        #if not k.getLabStatus(id).get('ready'):
        print(invitation_list)
        return JsonResponse(data=k.createLab(id,request.auth.key,email,invitation_list), status=200)
        #else:
        #    return JsonResponse(data={'warning':'A lab has already been deployed. No action has been taken'}, status=200)
    def get(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id)
        try:
            return JsonResponse(data=k.getLab(id,request.auth.key), status=200)
        except Exception as e:
            return JsonResponse(data={'error':e.__str__()}, status=404)
    
    def delete(self,request):
        lab = str(Token.objects.get(key=request.auth.key).user.id)
        try:
            return JsonResponse(data=k.deleteLab(lab), status=200)
        except:
            return JsonResponse(data={'error':'internal server error'}, status=500)

class volumeView(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id).__str__()
        email = Token.objects.get(key=request.auth.key).user.__str__()
        #comprueba que no haya pvc
        if(k.checkPVC(id) == None):
            k.createPVC(id)
        #elif(k.checkPV(id) == None):
        return JsonResponse(data=k.createPV(id,email), status=200)

    def get(self,request):
        lab = str(Token.objects.get(key=request.auth.key).user.id)
        try:
            return JsonResponse(data=k.getLab(lab), status=200)
        except:
            return JsonResponse(data={'error':'no lab has been found'}, status=404)
    
    def delete(self,request):
        lab = str(Token.objects.get(key=request.auth.key).user.id)
        try:
            return JsonResponse(data=k.deleteLab(lab), status=200)
        except:
            return JsonResponse(data={'error':'internal server error'}, status=500)

class serviceView(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id).__str__()
        return JsonResponse(data=k.createSvc(id), status=200)
    def get(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id).__str__()
        try:
            k.getSvcStatus(id,request.auth.key)
            return JsonResponse(data={'status':'alive'}, status=200)
        except:
            return JsonResponse(data={'error':'no svc has been found'}, status=404)
    
    def delete(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id).__str__()
        try:
            return JsonResponse(data=k.deleteSvc(id), status=200)
        except:
            return JsonResponse(data={'error':'internal server error'}, status=500)

class secretView(generics.CreateAPIView):
    #autentica
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id).__str__()
        return JsonResponse(data=k.createSvc(id), status=200)
    def get(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id).__str__()
        try:
            k.getSvcStatus(id,request.auth.key)
            return JsonResponse(data={'status':'alive'}, status=200)
        except:
            return JsonResponse(data={'error':'no svc has been found'}, status=404)
    
    def delete(self,request):
        id = str(Token.objects.get(key=request.auth.key).user.id).__str__()
        try:
            return JsonResponse(data=k.deleteSvc(id), status=200)
        except:
            return JsonResponse(data={'error':'internal server error'}, status=500)