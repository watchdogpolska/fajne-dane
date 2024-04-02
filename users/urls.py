from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='account-login'),
    path('examples/', views.ExamplesView.as_view(), name='examples-api'),
    path('register/', views.RegisterView.as_view(), name='account-register'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='account-reset-password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='account-change-password'),
    path('activate/', views.ActivateView.as_view(), name='account-activate'),
    path('logout/', views.logout_view, name='account-logout')
]
