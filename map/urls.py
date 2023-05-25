from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('', views.map_search, name='map_search'),

]
