from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/auth/', include('knox.urls')),
    path('api/register', views.UserCreate.as_view()),
    # path('api/modinfo', views.UserInfoCreate.as_view())
]
