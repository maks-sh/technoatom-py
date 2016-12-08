

if __name__ == '__main__':
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def condition(n, i):
        return True if n == 0 else i < n

    def fibonacci(n=0):
        if is_int(n):
            i, a, b = 0, 0, 1
            while condition(n, i):
                yield a
                i, a, b = i + 1, b, a + b

        else:
            print("Введите положительное число!")

    for n in fibonacci(10):
        print(n)