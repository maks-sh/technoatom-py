from django.contrib import admin
from finance.models import *

admin.site.register(Account)
admin.site.register(UserProfile)
admin.site.register(Charge)
admin.site.register(ChargeCategory)

# Register your models here.
