Репозиторий для домашних работ по факультативу "Программирование на Python"
=========================
Используемая версия Python: 3.5.2

Домашняя работа №1
---------------------------------
> Разработать класс Charge (денежная транзакция):
>
> - содержащий вычисляемый атрибут value - вещественное число, определяющее сумму денежной транзакции;
> - содержащий метод инициализации.
>
> После инициализации экземпляра класса, значение value изменять нельзя. Отрицательные значения соответствуют расходам, положительные - зачислениям на счет. Несмотря на реальные значения суммы транзакции, вычисляемые атрибут value не должен отдавать значения больше чем с двумя знаками после запятой. Используйте функцию round и либо декоратор, либо дескриптор на свое усмотрение.
>
> Разработать класс Account (банковский счет):
> - содержащий атрибут charges - список, определяющий последовательность денежных транзакций по счету;
> - содержащий атрибут total - вещественное число, определяющее текущее состояние счета;
> - содержащий метод инициализации;
> - содержащий методы добавления транзакций (приход и расход соответственно).
>
> Каждый элемент списка charges - экземпляр класса Charge. При инициализации экземпляра класса возможно задать начальное значение для состояния счета, по умолчанию - ноль. Атрибут total должен обновляться при вызове методов зачисления и списания, отрицательное значение атрибута невозможно.
>
> Дополнительно:
>
> Класс Account должен быть итерабелен (отдавать charges).

[Решение ДЗ №1](./hw_1/)

Домашняя работа №2
---------------------------------
> Определен следующий бесконечный генератор:
```python
from random import randint
from time import sleep
def events(max_delay, limit):
    while True:
        delay = randint(1, max_delay)
        if delay >= limit:
            sleep(limit)
            yield None
        else:
            sleep(delay)
            yield 'Event generated, awaiting %d s' % delay
```

>
>Генератор симулирует поступление событий в систему, на вход он получает максимальную задержку генерации max_delay для псевдослучайного времени ожидания и лимит времени ожидания. Если время ожидания превышает заданный лимит - генератор вернет значение None, что будет означать, что событий за интервал ожидания не произошло.
>
>Необходимо проинициализировать генератор (с произвольными параметрами) в глобальную переменную и определить класс WSGI-приложения, возвращающий события генератора. При этом в случае успеха (генератор вернул не None) приложение должно возвращать стутус 200 OK и строковое представление события, а в противном случае статус 204 No Content без тела сообщения.

[Решение ДЗ №2](./hw_2/)

Домашняя работа №3
---------------------------------
> Создать django-проект myfinance и django-приложение finance.
> Опеределить два маршрута:
> * Главная страница (корень r'^$')
> * Выписка по счету (например, r'^/charges/$')
>
> Главная страница должна содержать приветствие и ссылку на страницу выписки по счету.
> Страница выписки по счету должна содержать произвольную таблицу и ссылку на главную страницу.

[Решение ДЗ №3](./hw_3/)