from django.urls import path

from .views import (
    UserRegister, AccountActivate, TokenReactivate,
    Login, Logout,
    PasswordChange, PasswordResetRequest, PasswordReset,
    UserDetails
)


urlpatterns = [
    path('details/', UserDetails.as_view(), name='user_details'),
    path('register/', UserRegister.as_view(), name='user_register'),
    path('activate/resend/', TokenReactivate.as_view(), name='token_reactivate'),
    path('activate/', AccountActivate.as_view(), name='account_register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password/change/', PasswordChange.as_view(), name='password_change'),
    path('password/reset/request/', PasswordResetRequest.as_view(), name='password_reset_request'),
    path('password/reset/', PasswordReset.as_view(), name='password_reset'),
]
