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
        value_date = self.cleaned_data.get('date')
        if value_date is None:
            raise ValidationError('Введите правильное значение в поле "Дата"')
        value_amount = self.cleaned_data.get('amount')
        if value_amount is None:
            raise ValidationError('Введите правильное значение в поле "Сумма"')
        elif value_amount < 0:
            if value_date > date.today():
                raise ValidationError('Нельзя проводить списание в будущем!')
        # value_amount = Decimal(self.cleaned_data.get('amount')).quantize(Decimal('.00'))
        return cleaned_data
