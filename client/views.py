from logging import currentframe

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from writer.models import Article
from . models import Subscription


@login_required(login_url='my-login')
def client_dashboard(request):
    return render(request, 'client/client-dashboard.html')

@login_required(login_url='my-login')
def browse_articles(request):
    try:
        sub_details = Subscription.objects.get(user=request.user, is_active=True)
    except:
        return redirect('client-dashboard')

    current_subscription_plan = sub_details.subscription_plan

    articles = None

    if current_subscription_plan == 'Standard':
        articles = Article.objects.filter(is_premium=False)
    elif current_subscription_plan == 'Premium':
        articles = Article.objects.all()

    context = {'AllClientArticles': articles}

    return render(request, 'client/browse-articles.html', context)
