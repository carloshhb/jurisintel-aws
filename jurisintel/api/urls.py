
from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('case_data', views.receive_data, name='receive-data'),
    path('teste', views.teste, name='teste'),
]
