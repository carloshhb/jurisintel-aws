from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'conteudo'

urlpatterns = [
    path('', views.home, name='home'),
    url('upload/', views.file_upload, name='file-upload'),
    url('criar/', views.create, name='criar'),
    path('enviar/', views.upload, name='upload'),
    path('caso/<str:pk>', views.open_case, name='open-case'),
    path('caso/<str:pk>/similares', views.verify_similarities, name='similarities'),

    path('update-card/<str:pk>', views.card_update, name='card_update'),
    path('remove-card/<str:pk>', views.card_delete, name='card_delete'),
    path('add-doc/<str:pk>', views.AddDoc.as_view(), name='add-documento'),
]
