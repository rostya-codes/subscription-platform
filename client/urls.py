from django.urls import path

from . import views

urlpatterns = [
    path('client-dashboard', views.client_dashboard, name='client-dashboard'),
    path('browse-articles', views.browse_articles, name='browse-articles'),
]
