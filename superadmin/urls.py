from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    path('',           views.dashboard,     name='dashboard'),
    path('businesses/',views.businesses,    name='businesses'),
    path('users/',     views.users,         name='users'),
    path('licenses/',  views.licenses,      name='licenses'),
]