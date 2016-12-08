from django.conf.urls import url

from finance.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create-account/$', create_account, name='create_account'),
    url(r'^add/(?P<acc>\d{1,10})/$', charges_form, name='add_charges'),
    url(r'^info/(?P<acc>\d{1,10})/$', get_info, name='get_info'),
    url(r'^stat/(?P<acc>\d{1,10})/$', get_stat, name='get_stat'),
    url(r'^api/accounts$', AccountList.as_view(), name='account'),

]