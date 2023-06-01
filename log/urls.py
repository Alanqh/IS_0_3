from django.urls import path
from log.views import logout_view, index_login, profile, services, team

urlpatterns = [
    path('', index_login, name='index_login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('services/', services, name='services'),
    path('team/', team, name='team'),
]
