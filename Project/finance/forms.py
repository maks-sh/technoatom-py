# coding: utf8
from django.forms import Form, fields, widgets, ModelForm, DateInput, Textarea, DateField, DecimalField, NumberInput, CharField, TextInput, PasswordInput, EmailField
from django.forms.widgets import ChoiceInput
from finance.models import Account, Charge, UserProfile
from django.core.exceptions import ValidationError
import re
from decimal import *
from datetime import date
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ChargeForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ChargeForm, self).__init__(*args, **kwargs)
    #     try:
    #         print('sdsadasd', self.instance.user_id)
    #         self.fields['account'].queryset = Account.objects.filter(user_id=self.instance.user_id)
    #
    #     except:
    #         pass

    class Meta:
        fields = ['value', 'date', 'account', 'category']
        model = Charge
        widgets = {
            'value': NumberInput(attrs={'class': 'form___input',
                                    'Placeholder': '12345.00',
                                    'Pattern': '^[+-]?\d{0,5}(,\d{2})?$'},
                              ),
            'date': DateInput(attrs={'class': 'form___input',
                                    'type': 'date',
                                    'placeholder': 'гггг-мм-дд'}
                              ),
            # ToDo choice
            # 'account': ChoiceInput(attrs={'name:' }),
            #
            # 'category': ChoiceInput(attrs={'name:' })
        }
        labels = {
            'value': 'Сумма: ',
            'date': 'Дата: '
        }

    def clean(self):
        # ToDo сделать defclean
        cleaned_data = super().clean()
        print('charge:', self.cleaned_data.get('date'))
        value_date_cln = self.cleaned_data.get('date')
        value_value_cln = self.cleaned_data.get('value')
        value_value = self.data['value']
        value_date = self.data['date']

        def check(field, name):
            """Попытка реализовать проверку для Safari"""
            if field == '':
                err = 'Введите значение в поле "{}"'.format(name)
                return self.add_error(None, err)
            if name == 'Сумма':
                p = re.compile(r'^[+-]?(\d*)(?:\.(\d*))?$')
                result = p.match(field)

                if result is None:
                    err = 'Формат поля "{}": 12345.67 '.format(name)
                    return self.add_error(None, err)
                else:
                    if result.groups()[0] is not None and len(result.groups()[0]) > 5:
                        err = 'Максимальная сумма - 99999.99'
                        self.add_error(None, err)
                    if result.groups()[1] is not None and len(result.groups()[1]) > 2:
                        err = 'После точки должно быть не более двух цифровых знаков'
                        self.add_error(None, err)
                    return
            if name == 'Дата':
                pattern = re.compile(r'^(\d{4})\-(\d{2})\-(\d{2})$')
                results = pattern.match(field)
                print(results)
                if results is None:
                    err = 'Формат поля "{}": 2012-12-24 '.format(name)
                    return self.add_error(None, err)
                else:
                    try:
                        date(int(results.groups()[0]), int(results.groups()[1]), int(results.groups()[2]))
                    except:
                        err = 'Неправильно введена дата!'
                        return self.add_error(None, err)

        check(value_value, 'Сумма')
        check(value_date, 'Дата')

        if value_date_cln is not None and value_value_cln is not None and \
                value_value_cln < 0 and value_date_cln > date.today():
            self.add_error(None, 'Нельзя проводить списание в будущем!')
        return cleaned_data


class AccountForm(ModelForm):

    class Meta:
        fields = ['total', 'acc_name']
        model = Account

        labels = {
            'acc_name': 'Название счета: ',
            'total': 'Начальный баланс: '
        }

        widgets = {
            'acc_name': TextInput(attrs={'class': 'form___input',
                                        'Placeholder': 'Заначка',
                                         'size': '32'},
                                 ),
            'total': NumberInput(attrs={'class': 'form___input',
                                    'Placeholder': '12345,00',
                                    'Pattern': '^[+-]?\d{0,5}(,\d{2})?$'}
                                 )
        }


    def clean(self):
        # ToDo сделать defclean
        cleaned_data = super().clean()
        value_total = self.data['total']
        # print(value_total, value_acc_id)

        def check(field, name):
            """Попытка реализовать проверку для Safari"""
            if field == '':
                err = u'Введите значение в поле "{}"'.format(name)
                return self.add_error(None, err)
            if name == 'Сумма':
                p = re.compile(r'^[+-]?(\d*)(?:\.(\d*))?$')
                result = p.match(field)

                if result is None:
                    err = u'Формат поля "{}": 12345.67 '.format(name)
                    return self.add_error(None, err)
                else:
                    if result.groups()[0] is not None and len(result.groups()[0]) > 5:
                        err = u'Максимальная сумма - 99999.99'
                        self.add_error(None, err)
                    if result.groups()[1] is not None and len(result.groups()[1]) > 2:
                        err = u'После точки должно быть не более двух цифровых знаков'
                        self.add_error(None, err)
                    return

        check(value_total, 'Сумма')

        return cleaned_data


class UserCreateForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Password confirmation', widget=PasswordInput)

    class Meta:
        model = UserProfile

        fields = ['email', 'phone', 'last_name', 'first_name']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UpdateProfile(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone']

class UpdateAccount(ModelForm):
    class Meta:
        model = Account
        fields = ['acc_name','total']


class FilterForm(Form):
    date1 = DateInput()
    date2 = DateInput()
    class Meta:
        model = Charge
        fields = ['account']