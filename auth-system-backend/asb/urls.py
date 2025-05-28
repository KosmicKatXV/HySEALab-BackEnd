from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.UserCreate.as_view()),
    path('api/login/', views.Login.as_view()),
    path('api/auth/', obtain_auth_token, name='auth'),
    path('api/invitations/incoming',views.invitationView.as_view(), name='incoming'),
    path('api/invitations/outcoming>',views.invitationView.as_view(), name='outcoming'),
    path('k8s/', include('k8s.urls')),
    path('job_dispatcher/', include('job_dispatcher.urls')) 
]
