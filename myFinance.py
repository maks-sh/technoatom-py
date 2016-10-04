class ValueException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
        # как по хорошему делать исключения?

class Charge(object):
    def __init__(self, value):
        if type(value) == str or round(value, 2) - value != 0:
            raise ValueException(Exception, "Пожалуйста, введите правильное значение")
        else:
            self.__value = value # Когда переменная должна быть с двумя "_", а когда с одним? #
    # Надо ли размещать блок, что ниже, в ветку else? #
    value = property()
    @value.getter
    def value(self):
        return self.__value
    @value.setter
    def value(self, inpValue):
        raise ValueException(Exception, "Изменять значение операции запрещено!")

class Account(object):
    def __init__(self, total = 0):
        if total < 0:
            raise ValueException(Exception, "Пожалуйста, введите правильное значение! Нельзя открыть отрицательный счет")
        else:
            self.total = total
            self.charges = []
            self.current = 0

    def transaction(self, file):
        if self.total + file.value < 0:
            raise ValueException(Exception, "Не хватает денежных средств на счете для проведения операции!")
        else:
            self.total += file.value
            self.charges.append(file)

    def __iter__(self):
        for element in self.charges:
            yield element

# Почему в таком исполнении не нужен метод __next__?

#    def __next__(self):
#        if self.current > len(self.charges):
#            self.current = 0
#            raise StopIteration
#        next = self.current
#        self.current += 1
#        return next


myAccount = Account(1000)
print(myAccount.total, myAccount.charges)


breakfast = Charge(-300.11)
print(breakfast.value)
#breakfast.value = 12
print(breakfast.value)

salary = Charge(5000)

myAccount.transaction(breakfast)
myAccount.transaction(salary)
print(myAccount.total, myAccount.charges)

for transact in myAccount:
    print(transact)