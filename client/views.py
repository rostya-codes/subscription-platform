from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from account.models import CustomUser
from writer.models import Article
from . models import Subscription
from account.forms import UpdateUserForm
from . paypal import *


@login_required(login_url='my-login')
def client_dashboard(request):
    try:
        sub_details = Subscription.objects.get(user=request.user)
        current_subscription_plan = sub_details.subscription_plan
        is_active = sub_details.is_active
        context = {'SubPlan': current_subscription_plan, 'IsActive': is_active}
        return render(request, 'client/client-dashboard.html', context)
    except:
        current_subscription_plan = None
        is_active = False
        context = {'SubPlan': current_subscription_plan, 'IsActive': is_active}
        return render(request, 'client/client-dashboard.html', context)


@login_required(login_url='my-login')
def browse_articles(request):
    try:
        sub_details = Subscription.objects.get(user=request.user, is_active=True)
    except:
        return render(request, 'client/subscription-locked.html')

    current_subscription_plan = sub_details.subscription_plan

    articles = None

    if current_subscription_plan == 'Standard':
        articles = Article.objects.filter(is_premium=False)
    elif current_subscription_plan == 'Premium':
        articles = Article.objects.all()

    context = {'AllClientArticles': articles}

    return render(request, 'client/browse-articles.html', context)


@login_required(login_url='my-login')
def subscription_locked(request):
    return render(request, 'client/subscription-locked.html')


@login_required(login_url='my-login')
def subscription_plans(request):
    return render(request, 'client/subscription-plans.html')


@login_required(login_url='my-login')
def account_management(request):
    form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('client-account-management')

    try:
        sub_details = Subscription.objects.get(user=request.user)
        sub_id = sub_details.paypal_subscription_id

        context = {'UpdateUserForm': form, 'SubscriptionID': sub_id}

        return render(request, 'client/account-management.html', context)
    except:
        context = {'UpdateUserForm': form}

        return render(request, 'client/account-management.html', context)


@login_required(login_url='my-login')
def create_subscription(request, sub_id, plan):
    user = CustomUser.objects.get(pk=request.user.id)

    first_name = user.first_name
    last_name = user.last_name

    full_name = first_name + ' ' + last_name

    sub_cost = None

    if plan == 'Standard':
        sub_cost = '4.99'
    elif plan == 'Premium':
        sub_cost = '9.99'

    subscription = Subscription.objects.create(
        subscriber_name=full_name, subscription_plan=plan,
        subscription_cost=sub_cost, paypal_subscription_id=sub_id,
        is_active=True, user=user
    )

    context = {'SubscriptionPlan': plan}

    return render(request, 'client/create-subscription.html', context)


@login_required(login_url='my-login')
def delete_subscription(request, sub_id = None):

    try:
        # Delete subscription form PayPal
        access_token = get_access_token()
        cancel_subscription_paypal(access_token, sub_id)

        # Delete a subscription from Django
        subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=sub_id)
        subscription.delete()
    except Exception as e:
        print(e)

    return render(request, 'client/delete-subscription.html')
