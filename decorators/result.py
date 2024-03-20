from time import perf_counter
import functools
import requests
import re


def benchmark(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        value = func(*args, **kwargs)
        end = perf_counter()
        print(f'Время выполнения функции {func.__name__}: {end-start:.17f}')
        return value
    return wrapper


def logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        print(f'Функция вызвана с параметрами:\n{args}, {kwargs}')
        return value
    return wrapper


def counter(func):
    counter.count = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        counter.count += 1
        print(f'Функция была вызвана: {counter.count} раз')
        return value
    return wrapper


def memo(func):
    memo.cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0] in memo.cache:
            return memo.cache[args[0]]
        else:
            value = func(*args, **kwargs)
            memo.cache[args[0]] = value
            return value
    return wrapper


@counter
@logging
@benchmark
def word_count(word, url='https://www.gutenberg.org/files/2638/2638-0.txt'):
    # отправляем запрос в библиотеку Gutenberg и забираем текст
    raw = requests.get(url).text

    # заменяем в тексте все небуквенные символы на пробелы
    processed_book = re.sub('[\W]+', ' ', raw).lower()

    # считаем
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cлово {word} встречается {cnt} раз"


print(word_count('whole'))


def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)


if __name__ == "__main__":
    start = perf_counter()
    fibonacci(35)
    end = perf_counter()
    print(f'Время выполнения без кэширования: {end-start:.5f}')
    start = perf_counter()
    fibonacci = memo(fibonacci)
    fibonacci(35)
    end = perf_counter()
    print(f'Время выполнения с кэшированием: {end - start:.5f}')



