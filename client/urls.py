from django.urls import path

from . import views

urlpatterns = [
    path('client-dashboard', views.client_dashboard, name='client-dashboard'),
    path('browse-articles', views.browse_articles, name='browse-articles'),
    path('subscription-locked', views.subscription_locked, name='subscription-locked'),
    path('subscription-plans', views.subscription_plans, name='subscription-plans'),
    path('account-management', views.account_management, name='client-account-management'),

    # Subscription urls
    path('create-subscription/<sub_id>/<plan>', views.create_subscription, name='create-subscription'),
    path('delete-subscription/<sub_id>', views.delete_subscription, name='delete-subscription'),
    path('update-subscription/<sub_id>', views.update_subscription, name='update-subscription'),
    path('paypal-update-sub-confirmed', views.paypal_update_sub_confirmed, name='paypal-update-sub-confirmed'),
    path('django-update-sub-confirmed/<sub_id>', views.django_update_sub_confirmed, name='django-update-sub-confirmed'),

    # Account management
    path('delete-account', views.delete_account, name='client-delete-account'),
]
