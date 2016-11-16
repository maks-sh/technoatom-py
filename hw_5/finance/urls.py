from django.conf.urls import url

from finance.views import index, create_account, charges_form, get_info

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create-account/$', create_account, name='create_account'),
    url(r'^add/$', charges_form, name='add_charges'),
    url(r'^info/$', get_info, name='get_info'),
]