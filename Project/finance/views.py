#coding: utf8
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.db.models import Count, Sum
from .forms import ChargeForm, AccountForm, UserCreatForm
from .models import Account, Charge, UserProfile
from django.db.models.functions import Trunc
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout
#
from django.contrib import auth
from django.views.generic.edit import FormView
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated():
        return redirect('start')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        print(user)
        form=AuthenticationForm
        if user is None:
            print('пользователь не введен')
            print(username,password)
            return render(request,'login.html',{'form':form})

        else:
            print('Succ!')
            auth.login(request, user)
            return redirect('index')

@ensure_csrf_cookie
def reg(request):
    if request.user.is_authenticated():
        return redirect('start')
    else:
        if request.method == 'POST':
            user_form = UserCreatForm(request.POST)

            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password1'])
                # Save the User object
                new_user.save()
               # profile = UserProfile.objects.create(user=new_user)

                return redirect('/login/')
        else:
            user_form = UserCreatForm()
        return render(request, 'signup.html', {'form': user_form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def index(request):
    if request.user.is_authenticated():
        return redirect('start')
    else:
        response = render_to_response('index.html', {})
        return response

@transaction.atomic()
@ensure_csrf_cookie
def create_account(request):
    err = []
    if not request.user.is_authenticated():
        return redirect('index')
    if request.method == 'POST':

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
        #info = 'Заполните, пожалуйста, данные для транзакции'
        info = request.user.id
        form = AccountForm()
    return render(
        request, 'create_account.html',
        {'form': form,
         'info': info,
         'err': err
         }
    )

@transaction.atomic()
@ensure_csrf_cookie
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
    if Account.objects.filter(acc_id=acc).exists():
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

@transaction.atomic()
def start_page(request):
    if Account.objects.filter(user_id=request.user.id).exists():
        return redirect('create_account')
    else:
        pass
#         TOdo добавить информацию о счетах на этой странице
