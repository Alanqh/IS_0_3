from django.urls import path
from log.views import logout_view, index_login

urlpatterns = [
    path('', index_login, name='index_login'),
    path('logout/', logout_view, name='logout'),
]
