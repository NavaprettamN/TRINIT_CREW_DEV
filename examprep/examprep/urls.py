from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name='index'),
    path("signup/", views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('analytics/', views.analytics, name='analytics'),
    path('', views.logout, name='logout'),
    path('uploaddata', views.uploaddata, name='uploaddata'),
    path('manual', views.manual, name='manual'),
    path('uploadmanual', views.uploadmanual, name='uploadmanual'),
    path('taketest', views.taketest, name='taketest'),
]
