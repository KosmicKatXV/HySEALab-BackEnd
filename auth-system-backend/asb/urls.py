from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.UserCreate.as_view()),
    path('api/login/', views.Login.as_view()),
    path('api/auth/', obtain_auth_token, name='auth'),
    path('api/token/', views.getUserFromToken.as_view()),
    path('invitation/',views.invitationView.as_view()),
    path('invitation/incoming/<str:email>',views.incomingDelete.as_view()),
    path('invitation/outcoming/<str:email>',views.outcomingDelete.as_view()),
    path('k8s/', include('k8s.urls')),
    path('job_dispatcher/', include('job_dispatcher.urls')) 
]
