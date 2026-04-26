# accounts/urls.py
from django.urls import path
from . import views
app_name = 'tenants'
urlpatterns = [
path('onboarding/', views.onboarding, name='onboarding'),
]