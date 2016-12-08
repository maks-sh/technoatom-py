# coding: utf8
# from django.shortcuts import render
# from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.db.models import Count, Sum
from .forms import ChargeForm, AccountForm
from .models import Account, Charge
from django.db.models.functions import Trunc
from django.db import transaction
from .serializers import AccountSerializer
from rest_framework import generics

def index(request):
    response = render_to_response('index.html', {})
    return response

@transaction.atomic()
def create_account(request):
    err = []
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():

            account = form.save()
            print(account.id_acc)
            return redirect('get_info', account.id_acc)
        else:
            info = 'Форма заполнена некорректно'
            # err = form.errors.as_data()['__all__']
            # for e in err: print(e)
            # print(type(form.errors.as_json()))
            # err = form.errors.as_json().encode('utf-8')
            # for boundfield in form: print(boundfield.label, boundfield.errors)
    else:
        info = 'Заполните, пожалуйста, данные для транзакции'
        form = AccountForm()
    return render(
        request, 'create_account.html',
        {'form': form,
         'info': info,
         'err': err
         }
    )

@transaction.atomic()
def charges_form(request, acc):
    if Account.objects.filter(id_acc=acc).exists():
        if request.method == 'POST':
            info = 'Форма заполнена некорректно'
            form = ChargeForm(request.POST)

            if form.is_valid():
                a = Account.objects.get(id_acc=acc)
                charg = form.save(commit=False)
                tot = a.total + charg.value
                if tot < 0:
                    info = 'Недостаточно средств на счете для проведения транзакции'
                else:
                    info = 'Данные отправлены'
                    charg.account = a
                    charg.save()
                    a.total = tot
                    a.save()
                    # print(form.cleaned_data)
            else:
                print(form.data)
        else:
            info = 'Заполните, пожалуйста, данные для транзакции'
            form = ChargeForm()
        return render(
            request, 'charges_form.html',
            {'form': form,
             'info': info,
             'acc': acc}
        )
    else:
        return redirect('create_account')

@transaction.atomic()
def get_info(request, acc):
    if Account.objects.filter(id_acc=acc).exists():
        charges = Charge.objects.filter(account=acc)
        print(charges)
        transactions_pol = [i for i in charges if i.value > 0]
        transactions_otr = [i for i in charges if i.value < 0]
        return render(
            request, 'get_info.html',
            {'transactions_pol': transactions_pol,
             'transactions_otr': transactions_otr,
             'acc': acc}
        )
    else:
        return redirect('create_account')

@transaction.atomic()
def get_stat(request, acc):
    if Account.objects.filter(id_acc=acc).exists():
        change_by_month = Charge.objects \
            .filter(account_id=acc) \
            .annotate(month=Trunc('date', 'month')) \
            .values('month') \
            .annotate(c=Count('id')) \
            .annotate(s=Sum('value')) \
            .values('month', 'c', 's') \
            .order_by('month')
        # todo вставить недостающие элементы в список, т.е. вставить месяцы, когда не происходило транзакций


        return render(
            request, 'get_stat.html',
            {'acc': acc,
             'amount': Account.objects.get(id_acc=acc).total,
             'stat_data': change_by_month
             }
        )
    else:
        return redirect('create_account')

# todo сделать проверку на существование счета как декаратор

class AccountList(generics.ListAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()