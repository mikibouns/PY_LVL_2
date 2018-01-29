import sys
from functools import wraps

import log_config


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
        log_config.app_log.info('Module: %(modulename)s, function: %(funcname)s ==> START', params)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            params['error'] = str(e)
            log_config.app_log.error('Module: %(modulename)s, function: %(funcname)s, error: %(error)s', params)
        else:
            log_config.app_log.info('Module: %(modulename)s, function: %(funcname)s ==> END', params)
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