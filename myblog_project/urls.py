"""myblog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rammyblog.urls')),
    path('account/reset', views.PasswordResetView.as_view(
       template_name = 'rammyblog/password_reset_form.html', email_template_name = 'rammyblog/password_reset_email.html', subject_template_name = 'rammyblog/password_reset_subject.txt' ), 
    name = 'password_reset'
    ),

    path('account/reset/done', views.PasswordResetDoneView.as_view(
        template_name = 'rammyblog/password_reset_done.html'
        ), name = 'password_reset_done'),

    path('account/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name = 'rammyblog/password_reset_confirm.html'),
    name = 'password_reset_confirm'),


    path('account/reset/complete/',
    views.PasswordResetCompleteView.as_view(template_name='rammyblog/password_reset_complete.html'),
    name='password_reset_complete'), 

   path('settings/password/', views.PasswordChangeView.as_view(template_name='rammyblog/password_change.html'),
    name='password_change'),

   path('settings/password/done/', views.PasswordChangeDoneView.as_view(
    template_name='rammyblog/password_change_done.html'),
    name='password_change_done'
    ),

   path('login/', views.LoginView.as_view(), name = 'login' ),

   path ('logout/', views.LogoutView.as_view(), name = 'logout'),
   path('markdownx/', include('markdownx.urls'))


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
