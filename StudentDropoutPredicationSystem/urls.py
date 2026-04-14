# student_dropout_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns =[
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('academics/', include('academics.urls')),
    path('predictions/', include('predictions.urls')),
    path('counseling/', include('counseling.urls')),
    path('', lambda request: redirect('login')),
]