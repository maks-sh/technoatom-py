# from django.shortcuts import render
# from django.template import RequestContext, loader
# from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from .forms import ChargeForm, AccountForm
from .models import Account, Charge
from .generator import random_transactions
# Create your views here.

def index(request):
    response = render_to_response('index.html', {})
    return response


def create_account(request):

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():

            account = form.save()
            return redirect ('get_info',account.id_acc)
           # return render(
           #    request, 'get_info.html',
           #     {'acc':account.id_acc}
           # )
        else:
            info = 'Форма заполнена некорректно'
            print(form.data)
    else:
        info = 'Заполните, пожалуйста, данные для транзакции'
        form = AccountForm()
    return render(
        request, 'create_account.html',
        {'form': form,
         'info': info,
         }
    )


def charges_form(request, acc):
    if request.method == 'POST':
        info = 'Форма заполнена некорректно'
        form = ChargeForm(request.POST)

        if form.is_valid():
            a=Account.objects.get(id_acc=acc)
            charg = form.save(commit=False)
            tot=a.total+charg.value
            if tot<0:
                info='Недостаточно средств для проведения транзакции'
            else:
                info = 'Данные отправлены'
                charg.account = a
                charg.save()
                a.total=tot
                a.save()
            # print(form.cleaned_data)
        else:
            print(form.data)
    else:
        info ='Заполните, пожалуйста, данные для транзакции'
        form = ChargeForm()
    return render(
        request, 'charges_form.html',
        {'form': form,
         'info': info,
         'acc':acc}
    )


def get_info(request, acc):
    charges = Charge.objects.filter(account=acc)
    transactions_pol = [i for i in charges if i.value > 0]
    transactions_otr = [i for i in charges if i.value < 0]

    return render(
        request, 'get_info.html',
        {'transactions_pol': transactions_pol,
         'transactions_otr': transactions_otr,
         'acc':acc}
    )