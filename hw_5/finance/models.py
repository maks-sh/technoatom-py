from django.db import models
# Create your models here.


class Account(models.Model):
    id_acc = models.IntegerField(primary_key=True, db_index=False)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'Accounts'
        get_latest_by = 'id_acc'



class Charge(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, db_column='account')
    value = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField()

    class Meta:
        db_table = 'Charges'
