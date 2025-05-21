from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('deployment/', views.deploymentView.as_view()),
    path('volume/', views.volumeView.as_view()),
    path('lab/', views.LabView.as_view())
]
