# from django.shortcuts import render
# from django.template import RequestContext, loader
# from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from .forms import ChargeForm
from .generator import random_transactions
# Create your views here.


def index(request):
    response = render_to_response('index.html', {})
    return response


def charges_static(request):
    response = render_to_response('charges_static.html', {})
    return response


def charges_form(request):
    if request.method == 'POST':
        info = 'Форма заполнена некорректно'
        form = ChargeForm(request.POST)
        if form.is_valid():
            info = 'Все верно'
            print(form.cleaned_data)
        else:
            print(form.errors)
    else:
        info = 'Заполните, пожалуйста, данные для транзакции'
        form = ChargeForm()
    return render(
        request, 'charges_form.html',
        {'form': form,
         'info': info,
         }
    )


def charges_random(request):
    transactions = [i for i in random_transactions()]
    transactions_pol = [i for i in transactions if i[1] > 0]
    transactions_otr = [i for i in transactions if i[1] < 0]
    return render(
        request, 'charges_random.html',
        {'transactions_pol': transactions_pol,
         'transactions_otr': transactions_otr}
    )