from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('public/', views.public, name='public'),
    path('auth/', views.auth, name='auth'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
