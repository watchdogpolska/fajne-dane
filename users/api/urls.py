from django.urls import path

from .views import UserRegistration, AccountActivation

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('activate/', AccountActivation.as_view(), name='account_registration'),
]
