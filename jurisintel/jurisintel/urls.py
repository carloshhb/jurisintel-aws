"""prototipov2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
# from conteudo.admin import admin_site as temas_admin
from conteudo.admin import admin_site as cases_admin

from accounts import views as acc_views
from . import views

urlpatterns = [

    url(r'^reset/$', auth_views.PasswordResetView.as_view(
        template_name='accounts/registration/password_reset.html',
        email_template_name='accounts/registration/password_reset_email.html',
        subject_template_name='accounts/registration/password_reset_subject.txt'
    ), name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),

    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),

    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(
        template_name='accounts/registration/password_change.html'), name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/registration/password_change_done.html'), name='password_change_done'),

    path('admin/', admin.site.urls),
    # path('admin/', temas_admin.urls),
    path('admin/', cases_admin.urls),

    # OAUTH2 URLS
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    path('', views.index, name="home"),
    path('logout/', acc_views.user_logout, name='logout'),
    path('contato/', views.contato, name='contato'),
    path('home/', include('conteudo.urls')),
    path('contas/', include('accounts.urls')),
    path('api/', include('api.urls')),
]

admin.site.site_header = "Jurisintel Admin"
admin.site.site_title = "Jurisintel Admin Portal"
admin.site.index_title = "Jurisintel Administração"
