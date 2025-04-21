from django.urls import path, re_path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('logging/', views.logging, name='logging'),
    re_path(r'^honeypot(?:/(?P<path>.*))?$', views.honeypot, name='honeypot'),
]
