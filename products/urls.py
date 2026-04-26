from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',                views.list_view,    name='list'),
    path('add/',            views.add_view,     name='add'),
    path('<int:pk>/edit/',  views.edit_view,    name='edit'),
    path('<int:pk>/delete/',views.delete_view,  name='delete'),
    path('<int:pk>/toggle/',views.toggle_active,name='toggle'),
]