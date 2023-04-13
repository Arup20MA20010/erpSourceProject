from django.urls import path
from . import views


urlpatterns = [
    path('', views.userRegistration, name='landingPage'),
    path('home', views.home, name="home"),
    path('registration/', views.userRegistration, name='registration'),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout")
]
