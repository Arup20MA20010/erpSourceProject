from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('registration/', views.userRegistration, name='registration'),
    path('login/', views.loginView, name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout")
]
