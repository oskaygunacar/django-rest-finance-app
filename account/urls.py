from django.contrib import admin
from django.urls import path,include
from account import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('api-token/generate/', views.user_api_new_token_generate_view, name='user_api_new_token_generate_view'),
    path('api-token/', views.user_api_token, name='user_api_token'),
]