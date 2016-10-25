from datetime import date
from decimal import Decimal
from random import randint


def random_transactions():
    today = date.today()
    start_date = today.replace(month=1, day=1).toordinal()
    end_date = today.toordinal()
    while True:
        start_date = randint(start_date, end_date)
        random_date = date.fromordinal(start_date)
        if random_date >= today:
            break
        random_value = randint(-10000, 10000), randint(0, 99)
        random_value = Decimal('%d.%d' % random_value)
        yield random_date, random_value
