from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.FloatField(default=0.0)
    currencies = models.ManyToManyField('assets.Currency', through='assets.UserCurrency')

    def __str__(self):
        return self.user.username
