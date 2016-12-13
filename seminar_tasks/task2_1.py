from time import sleep
from random import randint
import slowlog


if __name__ == '__main__':
    def decorator_maker_with_arguments(decorator_arg1):
        print(decorator_arg1)
        def my_decorator(func):
            print(decorator_arg1)
            def wrapped(function_arg1):
                print(decorator_arg1, function_arg1)

                return
            return wrapped
        return my_decorator

    @decorator_maker_with_arguments(3)
    def some_func(message):
        delay = randint(1, 10)
        sleep(delay)
        print(message)
        return True


    some_func("sadsa")