from django.shortcuts import render, redirect
from django.http import HttpResponse
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


@login_required(login_url='my-login')
def update_subscription(request, sub_id):
    access_token = get_access_token()

    # approve_link = Hateoas link from PayPal
    approve_link = update_subscription_paypal(access_token, sub_id)
    if approve_link:
        return redirect(approve_link)
    else:
        return HttpResponse('Unable to obtain the approval link')


@login_required(login_url='my-login')
def paypal_update_sub_confirmed(request):
    try:
        sub_details = Subscription.objects.get(user=request.user)
        subscription_id = sub_details.paypal_subscription_id
        context = {'SubscriptionID': subscription_id}

        return render(request, 'client/paypal-update-sub-confirmed.html', context)
    except:
        return render(request, 'client/paypal-update-sub-confirmed.html')


@login_required(login_url='my-login')
def django_update_sub_confirmed(request, sub_id):
    access_token = get_access_token()
    current_plan_id = get_current_subscription(access_token, sub_id)
    if current_plan_id == 'P-4NS387979K059831DM7OXKXQ':  # Standard
        new_plan_name = 'Standard'
        new_cost = 4.99

        Subscription.objects.filter(paypal_subscription_id=sub_id).update(
            subscription_plan=new_plan_name,
            subscription_cost=new_cost
        )

    elif current_plan_id == 'P-9K333039403981241M7OXXEI':  # Premium
        new_plan_name = 'Premium'
        new_cost = 9.99

        Subscription.objects.filter(paypal_subscription_id=sub_id).update(
            subscription_plan=new_plan_name,
            subscription_cost=new_cost
        )

    return render(request, 'client/django-update-sub-confirmed.html')
