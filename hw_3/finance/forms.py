from django.forms import Form, fields, widgets
from django.core.exceptions import ValidationError
import re
from decimal import *
from datetime import date


class ChargeForm(Form):
    amount = fields.DecimalField(
        label='Сумма:',
        required=True,
        max_digits=7,
        decimal_places=2,
        widget=widgets.TextInput(
            attrs={'class': 'form___input',
                   'Placeholder': '12345.00',
                   'Pattern': '^[+-]?\d{0,5}(.\d{2})?$'
                   }
        )
    )

    # amount = fields.CharField(
    #     label='Сумма:',
    #     required=True, max_length=9,
    #     widget=widgets.Input(
    #         attrs={'class': 'form___input',
    #                'Placeholder': '12345.00',
    #                'Pattern': '^[+-]?\d{0,5}(.\d{2})?$'
    #                }
    #     )
    # )

    date = fields.DateField(
        label='Дата:',
        required=True,
        widget=widgets.DateInput(
            attrs={'class': 'form___input',
                   'type': 'date',
                   'placeholder': 'гггг-мм-дд'
                   }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        value_date_cln = self.cleaned_data.get('date')
        value_amount_cln = self.cleaned_data.get('amount')
        value_amount = self.data['amount']
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

        check(value_amount, 'Сумма')
        check(value_date, 'Дата')

        if value_date_cln is not None and value_amount_cln is not None and \
                value_amount_cln < 0 and value_date_cln > date.today():
            self.add_error(None, 'Нельзя проводить списание в будущем!')
        return cleaned_data
