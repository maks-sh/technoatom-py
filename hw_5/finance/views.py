# from django.shortcuts import render
# from django.template import RequestContext, loader
# from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from .forms import ChargeForm, AccountForm
from .models import Account, Charge


def index(request):
    response = render_to_response('index.html', {})
    return response


def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            acc = account.id_acc
            return redirect('/info/')
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


def charges_form(request):
    err = 0
    if request.method == 'POST':
        info = 'Форма заполнена некорректно'
        form = ChargeForm(request.POST)
        if form.is_valid():
            info = 'Все верно'
            charge = form.save(commit=False)
            try:
                charge.account = Account.objects.latest('id_acc')
                charge.save()
            except Warning:
                err = 'Не создано ни одного счета!'
        else:
            print(form.data)
    else:
        info = 'Заполните, пожалуйста, данные для транзакции'
        form = ChargeForm()
    return render(
        request, 'charges_form.html',
        {'form': form,
         'info': info,
         'err': err
         }
    )


def get_info(request):
    err = 0
    transactions_pol = []
    transactions_otr = []
    try:
        charges = Charge.objects.filter(account=Account.objects.latest('id_acc'))
        transactions_pol = [i for i in charges if i.value > 0]
        transactions_otr = [i for i in charges if i.value < 0]
    except Warning:
        err = 'Не создано ни одного счета!'

    return render(
        request, 'get_info.html',
        {'transactions_pol': transactions_pol,
         'transactions_otr': transactions_otr,
         'err': err}
    )