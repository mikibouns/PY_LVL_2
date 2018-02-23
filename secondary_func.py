import ipaddress
import sys
import os
import json
import argparse
import time


def get_msg(sock):
    data_msg = _convert_data(sock.recv(1024))
    return data_msg


def send_msg(sock, data):
    sock.send(_convert_data(data))


def _convert_data(data, encoding_type='utf-8'):
    '''
    Функция конвертирует полученные данные из bytes в dict и обратно в зависимости от входных данных,
    если типданных неверный, возвращает None
    :param data: входные данные
    :param encoding_type: тип кодировки
    :return: bytes or dict if error returns None
    >>> _convert_data({'hello': 'foo'})
    b'{"hello": "foo"}'
    >>> _convert_data(b'{"hello": "foo"}')
    {'hello': 'foo'}
    >>> _convert_data('hello world!')
    None
    '''
    if isinstance(data, bytes):
        try:
            data = json.loads(data.decode(encoding_type))
        except:
            data = None
    elif isinstance(data, dict):
        data['time'] = time.ctime(time.time())
        data = json.dumps(data).encode(encoding_type)
    elif isinstance(data, list):
        data = json.dumps(data).encode(encoding_type)
    else:
        data = None
    return data


def _check_ip(ip):
    '''
    Валидация ip адреса:
    >>> check_ip('192.168.1.1')
    True
    >>> check_ip('123456.3.5')
    False
    >>> check_ip(123)
    False
    '''
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True


def cl_options():
    help_cli = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description='CLI_app')

    parser.add_argument('--a',
                        type=str, default='127.0.0.1',
                        help='{} --a <addr> - IP-адрес (по умолчанию 127.0.0.1)'.format(help_cli))
    parser.add_argument('--p',
                        type=int, default='7777',
                        help='{} --p <port> - TCP-порт (по умолчанию использует порт 7777)'.format(help_cli))
    args = parser.parse_args()

    addr_port = {'addr': args.a, 'port': args.p}
    error = []

    if _check_ip(args.a):
        addr_port['addr'] = args.a
    else:
        error.append('!!!ip address is incorrect!!!')


    if int(args.p) <= 65535:
        addr_port['port'] = int(args.p)
    else:
            error.append('!!!port is incorrect, maximum allowable value 65535!!!')

    if error:
        return error
    else:
        return addr_port


if __name__ == '__main__':
    pass
