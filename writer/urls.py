from django.urls import path

from . import views

urlpatterns = [
    path('writer-dashboard', views.writer_dashboard, name='writer-dashboard'),
    path('create-article', views.create_article, name='create-article'),
]
