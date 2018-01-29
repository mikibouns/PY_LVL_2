import ipaddress
import sys
import json

from decorators import log


@log
def get_msg(sock):
    data_msg = _convert_data(sock.recv(1024))
    return data_msg

@log
def send_msg(sock, data):
    sock.send(_convert_data(data))


@log
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
        data = json.dumps(data).encode(encoding_type)
    else:
        data = None
    return data


@log
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


@log
def cl_srv_options(argv=sys.argv):
    '''
    srv.py -a <addr> -p <port>
    Параметры командной строки:
    -p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
    -a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)
    >>> cl_srv_options(['D:\IGOR\PYTHON\python_lvl2\python_lvl2_lesson2', '-a', '192.168.3.100', '-p', '55566'])
    {'addr': '192.168.3.100', 'port': 55566}
    >>> cl_srv_options(['D:\IGOR\PYTHON\python_lvl2\python_lvl2_lesson2'])
    {'addr': '0.0.0.0', 'port': 7777}
    '''
    addr_port = {'addr': '0.0.0.0', 'port': 7777}
    error = []
    for item, value in enumerate(argv):

        if value == '?':
            error.append('''
    Для получения справки: client.py ?

    srv.py -a <addr> -p <port>
    Параметры командной строки:
    -p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
    -a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)
            ''')
            break

        if value == '-a':
            try:
                argv[item + 1]
            except IndexError:
                error.append('!!!enter the ip address!!!')
                continue
            else:
                if _check_ip(argv[item + 1]):
                    addr_port['addr'] = argv[item + 1]
                else:
                    error.append('!!!ip address is incorrect!!!')

        elif value == '-p':
            try:
                argv[item + 1]
            except IndexError:
                error.append('!!!enter the port!!!')
                continue
            else:
                if argv[item + 1].isdigit():
                    if int(argv[item + 1]) <= 65535:
                        addr_port['port'] = int(argv[item + 1])
                    else:
                        error.append('!!!port is incorrect, maximum allowable value 65535!!!')
                else:
                    error.append('!!!port is incorrect, the value must consist of digits!!!')
    if error:
        return error
    else:
        return addr_port


@log
def cl_client_options(argv=sys.argv):
    '''
    client.py <addr> [<port>]
    Параметры командной строки:
    <port> - TCP-порт для работы (по умолчанию использует порт 7777)
    <addr> - IP-адрес(по умолчанию 127.0.0.1)
    Функция возвращает словать со значениями ip-адреса и tcp-порта,
    если параметры не переданны, функция возвращает адрес и порт по умолчанию (address: 127.0.0.1, port: 7777),
    если параметры неверны, возвращает список с сообщениями об ошибках.
    >>> cl_client_options(['D:\IGOR\PYTHON\python_lvl2\python_lvl2_lesson2', '192.168.3.100', '55566'])
    {'addr': '192.168.3.100', 'port': 55566}
    '''
    addr_port = {'addr': '127.0.0.1', 'port': 7777}
    error = []
    for item, value in enumerate(argv):
        if item == 1:
            if value == '?':
                error.append('''
    Для получения справки: client.py ?

    client.py <addr> [<port>]
    Параметры командной строки:
    <port> - TCP-порт для работы (по умолчанию использует порт 7777)
    <addr> - IP-адрес(по умолчанию 127.0.0.1)
                   ''')
            elif _check_ip(value):
                addr_port['addr'] = value
            else:
                error.append('!!!ip address is incorrect!!!')
        if item == 2:
            if value.isdigit():
                if int(value) <= 65535:
                    addr_port['port'] = int(value)
                else:
                    error.append('!!!port is incorrect, maximum allowable value 65535!!!')
            else:
                error.append('!!!port is incorrect, the value must consist of digits!!!')
    if error:
        return error
    else:
        return addr_port


if __name__ == '__main__':
    answear = _convert_data({'data': 'hello'})
    _check_ip('192.168.1.1')
    cl_srv_options(['D:\IGOR\PYTHON\python_lvl2\python_lvl2_lesson2', '-a', '192.168.3.100', '-p', '55566'])
    cl_client_options(['D:\IGOR\PYTHON\python_lvl2\python_lvl2_lesson2', '192.168.3.100', '55566'])