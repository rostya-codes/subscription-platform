from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('my-login', views.my_login, name='my-login'),
    path('user-logout', views.user_logout, name='user-logout'),

    # Password management
    # 1 - Allow us to enter our email in order to receive a password reset link
    path('reset-password', auth_views.PasswordResetView.as_view(template_name='account/password-reset.html'), name='reset_password'),
    # 2 - Show a success message stating that an email was sent to reset our password
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password-reset-sent.html'), name='password_reset_done'),
    # 3 - Send a link to our email, so that we can reset our password + We will be prompted to enter a new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password-reset-form.html'), name='password_reset_confirm'),
    # 4 - Show a success message stating that our password was changed
    path('password_reset_coplete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password-reset-complete.html'), name='password_reset_complete'),
]
