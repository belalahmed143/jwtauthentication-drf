from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('reset-password-email-send/', PasswordResetEmailSendView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', PasswordResetView.as_view(), name='reset-password'),

]