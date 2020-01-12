"""samplesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include

urlpatterns = [
    path('bboard/', include('bboard.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(next_page='bboard:index'), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(
            template_name='registration/change_password.html'),
         name='password_change'),
    path('accounts/password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='registration/password_changed.htm'),
         name='password_changed_done')
    path('accounts/password_reset/',
         PasswordResetView.as_view(
            template_name='registration/reset_password.html',
             subject_template_name='registration/reset_subject.txt',
             email_template_name='registration/reset_email.html'),
            name='password_reset'),
    path('accounts/password_reset/done/',
         PasswordResetDoneView.as_view(
            template_name='registration/email_sent.html'),
             name="password_reset_done"),
    path('accounts/reset/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(
             template_name = 'registration/confirm_password.html'),
            name='password_reset_confirm'),
    path('accounts/reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='registration/password_complete.html'),
            name='password_reset_complete'),
]

LOGOUT_REDIRECT_URL = 'bboard:index'
