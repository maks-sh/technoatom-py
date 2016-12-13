from django.db import models
from  django.contrib.auth.models import AbstractUser, PermissionsMixin
# Create your models here.


class Account(models.Model):
    acc_id = models.AutoField(primary_key=True, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    acc_name = models.CharField('account name', max_length=32, unique=False)
    user_id = models.ForeignKey('UserProfile', on_delete=models.CASCADE, db_column='id')

    class Meta:
        db_table = 'Accounts'


class Charge(models.Model):
    ch_id = models.AutoField(primary_key=True, blank=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE, db_column='acc_id')
    category = models.ForeignKey('ChargeCategory', on_delete=models.CASCADE, db_column='cat_id')

    class Meta:
        db_table = 'Charges'


class UserProfile(AbstractUser):
    phone = models.CharField('phone',max_length=255, unique=False)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField('phone',max_length=255, unique=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table='UserProfile'


class ChargeCategory(models.Model):
    cat_id = models.AutoField(primary_key=True, blank=True)
    cat_name = models.CharField('category', max_length=32, unique=False)