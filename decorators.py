import time

def check_time_decorator(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        print(f'Время выполнения функции {func.__name__} равно {end_time - start_time}')
        return result
    return wrapper