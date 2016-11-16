from django.forms import Form, fields, widgets, ModelForm, DateInput, Textarea, DateField, DecimalField, NumberInput
from finance.models import Account, Charge
from django.core.exceptions import ValidationError
import re
from decimal import *
from datetime import date


class ChargeForm(ModelForm):

    class Meta:
        fields = ['value', 'date']
        model = Charge
        widgets = {
            'value': NumberInput(attrs={'class': 'form___input',
                                    'Placeholder': '12345.00',
                                    'Pattern': '^[+-]?\d{0,5}(,\d{2})?$'},
                              ),
            'date': DateInput(attrs={'class': 'form___input',
                                    'type': 'date',
                                    'placeholder': 'гггг-мм-дд'}
                              )
        }
        labels = {
            'value': 'Сумма: ',
            'date': 'Дата: '
        }

    def clean(self):
        cleaned_data = super().clean()
        print('charge:', self.cleaned_data.get('date'))
        print('account data:', self.data)
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
        fields = '__all__'
        model = Account

        labels = {
            'id_acc': 'Номер счета: ',
            'total': 'Начальный баланс: '
        }

        widgets = {
            'id_acc': NumberInput(attrs={'class': 'form___input',
                                        'Placeholder': '12345',
                                        'Pattern': '^\d{0,5}$'},
                                 ),
            'total': NumberInput(attrs={'class': 'form___input',
                                    'Placeholder': '12345,00',
                                    'Pattern': '^[+-]?\d{0,5}(,\d{2})?$'}
                                 )
        }


        # date = fields.DateField(
        #     label='Дата:',
        #     required=True,
        #     widget=widgets.DateInput(
        #         attrs={'class': 'form___input',
        #                'type': 'date',
        #                'placeholder': 'гггг-мм-дд'
        #                }
        #     )
        # )
        #

    def clean(self):
        cleaned_data = super().clean()
        print('account data:', self)
        value_total = self.data['total']
        value_id_acc = self.data['id_acc']
        # print(value_total, value_id_acc)

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

        check(value_total, 'Сумма')
        check(value_id_acc, 'Номер счета')

        return cleaned_data
