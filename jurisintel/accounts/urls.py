from django.conf.urls import url

from accounts import views
from django.urls import path
from .views import PerfilView, RegistroTrial, AssinaturasView, EscritorioView
# SET THE NAMESPACE!
app_name = 'accounts'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    # url('registro/',views.registro,name='registro'),
    url('registro/', RegistroTrial.as_view(template_name='accounts/registro_trial.html'), name='registro'),
    url('entrar/', views.user_login, name='user_login'),
    url(r'reset/$', views.reset_password, name='reset_password'),
    url(r'perfil/$', PerfilView.as_view(template_name='accounts/perfil.html'), name='perfil'),
    url(r'perfil/assinatura$', AssinaturasView.as_view(template_name='accounts/profile_plans.html'), name='profile_plans'),
    url(r'perfil/escritorio$', EscritorioView.as_view(template_name='accounts/firm_view.html'), name='escritorio'),
    url(r'alterar-senha/', views.change_password, name='change_password'),
    url(r'add-tema/', views.add_temas_observe, name='add-temas'),

    path('agendamento/', views.agendamento, name='agendamento'),
    path('intro/', views.video_intro, name='video-intro'),
    path('first-step/<str:mode>', views.onboard_first_step, name='onboard_first_step')
]
