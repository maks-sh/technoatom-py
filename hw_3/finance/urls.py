from django.conf.urls import url

from finance.views import index, charges_static, charges_form, charges_random

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^charges-static/$', charges_static, name='static_table'),
    url(r'^add/$', charges_form, name='add_charges'),
    url(r'^charges/$', charges_random, name='charges_random'),
]