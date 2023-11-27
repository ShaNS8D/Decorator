from functools import wraps
import datetime
import os


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f'Дата и время вызова функции: {datetime.datetime.now()}\n')
                f.write(f'Имя функции: {old_function.__name__}\n')
                f.write(f'Аргументы: {args}, {kwargs}\n')
                f.write(f'Возвращаемое значение: {result}\n\n')
            return result
        return new_function
    return __logger

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:        
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Function should return 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Should return an integer'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'File {path} should exist'

        with open(path, encoding='utf-8') as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'Function name should be in the log'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} should be written to the file'


if __name__ == '__main__':
    test_2()