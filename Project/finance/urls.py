from django.conf.urls import url
from django.contrib.auth.views import logout as log

from finance.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create-account/$', create_account, name='create_account'),
    # url(r'^add/(?P<acc>\d{1,10})/$', charges_form, name='add_charges'),
    url(r'^add/$', charges_form, name='add_charges'),
    url(r'^info/$', get_info, name='get_info_all'),
    url(r'^info/(?P<acc>\d{1,10})/$', get_info, name='get_info'),
    url(r'^stat/$', get_stat, name='get_stat_all'),
    url(r'^stat/(?P<acc>\d{1,10})/$', get_stat, name='get_stat'),
    url(r'^signup/$', reg),
    url(r'^login/$', login_view, name='login'),
    url(r'^start/$', start_page, name='start'),
    url(r'^logout/$', log, {'template_name': 'index.html', 'next_page': '/'}, name='logout'),
    url(r'^user/$', user_edit, name='user_edit'),
    url(r'^confirm/(?P<activ_key>.{1,40})/$', confirmation, name='confirm'),
    url(r'^del-acc/(?P<acc>\d{1,10})/$', del_acc, name='delete_account'),
    url(r'^edit-acc/(?P<acc>\d{1,10})/$', acc_edit, name='edit_account'),
    url(r'^del-chg/(?P<chg>\d{1,10})/$', del_charge, name='delete_charge'),
    # url(r'^edit-chg/(?P<chg>\d{1,10})/$', chg_edit, name='edit_charge'),

]