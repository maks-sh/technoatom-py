from django.conf.urls import url

from finance.views import index, charges

urlpatterns = [
    url(r'^$', index),
    url(r'^charges/$', charges),
]