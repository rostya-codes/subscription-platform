import requests
import json

from . models import Subscription
from config import client_id, secret_key


def get_access_token():
    data = {'grant_type': 'client_credentials'}
    headers = {'Accept': 'application/json', 'Accept-Language': 'en-US'}

    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    r = requests.post(url, auth=(client_id, secret_key), headers=headers, data=data).json()

    access_token = r['access_token']

    return access_token


def cancel_subscription_paypal(access_token, sub_id):
    bearer_token = 'Bearer ' + access_token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + sub_id + '/cancel'
    r = requests.post(url, headers=headers)

    print(r.status_code)
