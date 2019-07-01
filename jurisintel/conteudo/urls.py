from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'conteudo'

urlpatterns = [
    path('', views.home, name='home'),
    url('upload/', views.file_upload, name='file-upload'),
    url('criar/', views.create, name='criar'),
    path('enviar/', views.upload, name='upload'),
    path('caso/<str:pk>', views.open_case, name='open-case'),
    path('caso/<str:pk>/similares', views.verify_similarities, name='similarities'),
    path('caso/<str:pk>/precedents', views.precedents, name='precedents'),

    path('search=<str:word>', views.filter_by_word, name='filter-cases-word'),
    path('search-sentence=<str:sentence>', views.filter_by_sentence, name='filter-cases-sentence'),
    path('search/<str:sentence>', views.filter_by_anything, name='filter-anything'),
    path('tema/<str:pk>/', views.open_tema, name='open-tema'),
    path('tema/<str:pk>/precedents/', views.conteudo_juridico, name='temas-precedents'),

    path('update-card/<str:pk>', views.card_update, name='card_update'),
    path('remove-card/<str:pk>', views.card_delete, name='card_delete'),
    path('add-tag/<str:pk>', views.add_card_tags, name='add_card_tags'),
    path('add-doc/<str:pk>', views.AddDoc.as_view(), name='add-documento'),
    path('rem-doc/<str:pk>', views.remover_arquivo, name='remover_arquivo'),
]
