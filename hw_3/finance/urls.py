from django.conf.urls import url

from finance.views import index, charges_static, charges_form, charges_random, j_login, j_rest, j_register, j_register_rest, j_booking

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^charges-static/$', charges_static, name='static_table'),
    url(r'^add/$', charges_form, name='add_charges'),
    url(r'^charges/$', charges_random, name='charges_random'),
    url(r'^j-login/$', j_login, name='j'),
    url(r'^j-rest/$', j_rest, name='j'),
    url(r'^j-register/$', j_register, name='j'),
    url(r'^j-register-rest/$', j_register_rest, name='j'),
    url(r'^j-booking/$', j_booking, name='j'),

]