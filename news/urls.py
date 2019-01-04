""" https://docs.djangoproject.com/en/2.1/topics/http/urls/ """

from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recent/', views.recent, name='recent'),
    path('about/', views.about, name='about'),
    path('<str:domain>/', views.site_index, name='site_index'),
    path('<str:domain>/recent/', views.site_recent, name='site_recent'),
    path('text/<int:id>/', views.text, name='text')
]
