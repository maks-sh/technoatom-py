#coding: utf8
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.db.models import Count, Sum
from .forms import ChargeForm, AccountForm, UserCreateForm, UpdateProfile
from .models import Account, Charge, UserProfile
from django.db.models.functions import Trunc
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime, hashlib, random
from django.contrib import auth
from django.views.generic.edit import FormView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail

#TODO сделать редактирование нормально, погуглить
@login_required()
def user_edit(request):
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST,instance=request.user)
        if form.is_valid():
            print("Succ!")
            form.save()
            return redirect('start')
    else:
        form = UpdateProfile(instance=request.user)

    args['form'] = form
    return render(request, 'edit_profile.html', args)


def confirmation(request,activ_key):
    if UserProfile.objects.filter(activation_key=activ_key).exists():
        user = UserProfile.objects.get(activation_key=activ_key)
        user.is_active=True
        user.save()
        return render(request,'activate.html')


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
            user_form = UserCreateForm(request.POST)

            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password1'])
                username = user_form.cleaned_data['first_name']
                user_email = user_form.cleaned_data['email']
                salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
                activation_key = hashlib.sha1((salt + user_email).encode('utf-8')).hexdigest()
                key_expires = datetime.datetime.today() + datetime.timedelta(2)
                # Get user by username
                # Create and save user profile
                # Send email with activation key
                email_subject = 'Подтверждение регистрации'
                email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
                48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)
                print(email_body)
                send_mail(email_subject, email_body, 'emrozenfeld@yandex.ru',
                            [user_email])

                # Save the User object
                new_user.save()
                profile = UserProfile.objects.get(email=user_email)
                profile.key_expires=key_expires
                profile.activation_key=activation_key
                profile.is_active=False
                profile.save()

                return render_to_response('registration_complete.html', {})
        else:
            user_form = UserCreateForm()
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
        form = AccountForm(request.POST)
        if form.is_valid():

            account = form.save(commit=False)
            account.user_id=UserProfile.objects.get(id=request.user.id)
            account.save()
            print(account.acc_id)
            return redirect('get_info', account.acc_id)
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
@ensure_csrf_cookie
@login_required(login_url='index')
def charges_form(request):

    if request.method == 'POST':
        info = 'Форма заполнена некорректно'
        form = ChargeForm(request.POST)

        if form.is_valid():
            charg = form.save(commit=False)
            form.save()
            a = charg.account
            tot = a.total + charg.value
            if tot < 0:
                info = 'Недостаточно средств на счете для проведения транзакции'
            else:
                info = 'Данные отправлены'
                charg.save()
                a.total = tot
                a.save()
                return redirect('start')
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
        }
    )

@transaction.atomic()
@login_required()
def get_info(request, acc=0):
    if acc !=0:
        if not Account.objects.filter(acc_id=acc).exists():
            return redirect('start')
        if Account.objects.get(acc_id=acc).user_id != request.user.id:
            return redirect('start')
        if Account.objects.filter(acc_id=acc).exists():
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
    else:
        charges = Charge.objects.filter(account__user_id_id=request.user.id)
        print(charges)
        transactions_pol = [i for i in charges if i.value > 0]
        transactions_otr = [i for i in charges if i.value < 0]
        return render(
            request, 'get_info.html',
            {'transactions_pol': transactions_pol,
             'transactions_otr': transactions_otr,
             'acc': acc}
        )

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
             'amount': Account.objects.get(acc_id=acc).total,
             'stat_data': change_by_month
             }
        )
    else:
        return redirect('create_account')

# todo сделать проверку на существование счета как декаратор

@transaction.atomic()
def start_page(request):

    accs = Account.objects.filter(user_id=request.user.id).all()
    for a in accs:
        a.charges = Charge.objects.filter(account=a.acc_id).all()[:5]
        print(Charge.objects.filter(account=a.acc_id).all()[:5])
        print(a.acc_id)

    if not Account.objects.filter(user_id=request.user.id).exists():
        return redirect('create_account')
    else:
        return render(
            request, 'start.html',

            {'accs': accs}
        )
#         TOdo добавить информацию о счетах на этой странице