import socket
import time

from secondary_func import cl_srv_options, get_msg, send_msg
from data_base import SERVICE_MSG, users_list

class CeateSrvSocket:
    '''
    Менеджер контекста для создания сокета, гарантированно закрывает сокет.
    Выводит информацию об ошибке.
    '''

    def __init__(self, addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((addr, port))
        self.sock.listen(5)

    def __enter__(self):
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print('{}: {}'.format(exc_type, exc_val))
        self.sock.close()
        return True


class Srv:
    def auth_user(self, data):
        pass

    def disabling_user(self, data):
        users_list[data['account_name']]['state'] = 'offline'
        print('User {} is offline!'.format(data['account_name']))
        return SERVICE_MSG['quit']

    def check_user_name(self, data):
        user_name = data['user']['account_name'].lower()
        if user_name in users_list:
            for item, value in users_list.items():
                print('{} >> {}'.format(item, value['state']))
            return SERVICE_MSG['4xx'][409]
        # else:
        #     users_list[user_name] = {'passwd': None,
        #                              'status': 'unauthorized',
        #                              'state': 'online'}
        #     for item, value in users_list.items():
        #         print('{} >> {}'.format(item, value['state']))
        #     return SERVICE_MSG['2xx'][200]
        return {}

    def presence_check(self):
        data = {"action": "probe"}
        data['time'] = time.ctime(time.time())
        return data

    def srv_response(self, data):
        response = {}
        if 'action' in data:
            # Присутствие. Сервисное сообщение для извещения сервера о присутствии клиента​ online
            if data['action'] == 'presence':
                response = self.check_user_name(data)
            # ​Простое​ сообщение​ пользователю​ или​ в​ чат
            elif data['action'] == 'msg':
                pass
            # Отключение от сервера
            elif data['action'] == 'quit':
                response = self.disabling_user(data)
            # Авторизация на сервере
            elif data['action'] == 'authenticate':
                response = self.auth_user(data)
            # Присоединиться к чату
            elif data['action'] == 'join':
                pass
            # Покинуть чат
            elif data['action'] == 'leave':
                pass

            elif data['action'] == 'test':
                response = {'action': 'test'}

            response['time'] = time.ctime(time.time())
            return response


def main():
    srv = Srv()
    data = cl_srv_options()
    if isinstance(data, dict):
        with CeateSrvSocket(data['addr'], data['port']) as sock:
            conn, addr = sock.accept()
            with conn:
                send_msg(conn, srv.presence_check())
                while True:
                    data_msg = get_msg(conn)
                    print(data_msg)
                    if data_msg:
                        response = srv.srv_response(data_msg)
                        time.sleep(1)
                        send_msg(conn, response)
                    elif data is None:
                        continue
                    else:
                        break

    else:
        for i in data:
            print(i)


if __name__ == '__main__':
    main()


