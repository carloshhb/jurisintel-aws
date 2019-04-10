from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'conteudo'

urlpatterns = [
    url('upload/', views.file_upload, name='file-upload'),
    url('criar/', views.create, name='criar'),
    url('remover/', views.remove, name='remover-cartao'),
    path('enviar/', views.upload, name='upload'),
    path('caso/<str:pk>', views.open_case, name='open-case'),
    path('caso/<str:pk>/similares', views.verify_similarities, name='similarities'),
]
