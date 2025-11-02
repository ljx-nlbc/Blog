from django.urls import path,include
from . import views

app_name='accounts'
urlpatterns=[
    #django默认的身份验证
    path('',include('django.contrib.auth.urls')),
    path('register/',views.register,name='register'),
]