from django.urls import path

from . import views

urlpatterns = [
    path('client-dashboard', views.client_dashboard, name='client-dashboard'),
    path('browse-articles', views.browse_articles, name='browse-articles'),
    path('subscription-locked', views.subscription_locked, name='subscription-locked'),
    path('subscription-plans', views.subscription_plans, name='subscription-plans'),
    path('account-management', views.account_management, name='client-account-management'),
    path('create-subscription/<sub_id>/<plan>', views.create_subscription, name='create-subscription'),
]
