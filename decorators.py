import sys
from functools import wraps
import logging

import log_config

app_log = logging.getLogger('app')

def log(func):
    '''
    Декоратор записывает информацию о старте, завершении и ошибке обернутой ф-ции.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        params = {
            'funcname': func.__name__,
            'modulename': sys.argv[0],
            'error': ''
        }
        app_log.info('Module: %(modulename)s, function: %(funcname)s ==> START', params)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            params['error'] = str(e)
            app_log.error('Module: %(modulename)s, function: %(funcname)s, error: %(error)s', params)
        else:
            app_log.info('Module: %(modulename)s, function: %(funcname)s ==> COMPLETED', params)
            return result
    return wrapper


if __name__ == '__main__':
    @log
    def func():
        return 2 + 2

    @log
    def func_1():

        return 1 + 'a'

    @log
    def func_2():
        return 2 / 0

    print(func())
    print(func_1())
    print(func_2())