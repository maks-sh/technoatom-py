from django.conf.urls import url

from finance.views import index, charges_static, charges

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^charges-static/$', charges_static, name='static_table'),
    url(r'^charges/$', charges, name='charges'),
]