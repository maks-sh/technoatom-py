from django.conf.urls import url
from django.contrib.auth.views import logout as log

from finance.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create-account/$', create_account, name='create_account'),
    # url(r'^add/(?P<acc>\d{1,10})/$', charges_form, name='add_charges'),
    url(r'^add/$', charges_form, name='add_charges'),
    url(r'^info/(?P<acc>\d{1,10})/$', get_info, name='get_info'),
    url(r'^stat/(?P<acc>\d{1,10})/$', get_stat, name='get_stat'),
    url(r'^signup/$', reg),
    url(r'^login/$', login_view, name='login'),
    url(r'^start/$', start_page, name='start'),
    url(r'^logout/$', log, {'template_name': 'index.html', 'next_page': '/'}, name='logout'),
    url(r'^user/$', user_edit, name='user_edit'),
]