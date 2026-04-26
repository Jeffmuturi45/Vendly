from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('',     views.index, name='home'),
    path('demo/', views.enter_demo,  name='demo'),
]