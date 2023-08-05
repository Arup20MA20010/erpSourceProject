from django.urls import path
from . import views


urlpatterns = [
    path('', views.userRegistration, name='landingPage'),
    path('generate_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('home', views.home, name="home"),
    path('registration/', views.userRegistration, name='registration'),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('activate/<uidb64>/<token>/',views.ActivateAccount.as_view(),name='activate'),
]
