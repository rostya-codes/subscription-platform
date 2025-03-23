from django.db import models

from account.models import CustomUser


class Subscription(models.Model):
    subscriber_name = models.CharField(max_length=300)
    subscription_plan = models.CharField(max_length=255)
    subscription_cost = models.CharField(max_length=255)

    paypal_subscription_id = models.CharField(max_length=300)

    is_active = models.BooleanField(default=False)

    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, max_length=10)

    def __str__(self):
        return f'{self.subscriber_name} - {self.subscription_plan} subscription'
