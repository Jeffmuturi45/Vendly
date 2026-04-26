from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('pos/',            views.pos_view,    name='pos'),
    path('',                views.list_view,   name='list'),
    path('<int:pk>/',       views.detail_view, name='detail'),
]