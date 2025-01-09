from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log, name='eventlog-home'),
    path('', views.kev, name='KEV-home'),
    path('search/', views.search, name="search")
]