from contextlib import contextmanager
import socket
import time

from secondary_func import cl_client_options, get_msg, send_msg


class Client:
    def __init__(self):
        self.account_name = None
        self.password = None

    def menu(self):
        print('    HELLO {}!!!'.format(self.account_name.upper()))
        while True:
            print('''
    ######################## MENU ########################
    1. Users list
    2. User to user
    3. User to chat
    4. Authorization
    5. Quit
    ######################################################
            ''')
            data = input('Enter the number of menu: ')
            if not data.isdigit():
                continue
            elif data == '1':
                print('Ok')
            elif data == '2':
                print('Ok')
            elif data == '3':
                print('Ok')
            elif data == '4':
                print('Ok')
            elif data == '5':
                return self.quit()

    def create_user_name(self):
        while True:
            self.account_name = input('Enter your username: ')
            if len(self.account_name) < 10:
                return self.service_msg()

    def client_response(self, data):
        if isinstance(data, dict):
            if 'action' in data:
                if data['action'] == 'probe':
                    data = self.service_msg()
                elif data['action'] == 'msg' and data['to'][0] == '#':
                    data = self.user_to_chat()
                elif data['action'] == 'msg':
                    data = self.user_to_user()

            elif 'response' in data:
                if data['response'] == 200:
                    data = self.menu()

                elif data['response'] == 201:
                    pass
                elif data['response'] == 202:
                    pass
                elif data['response'] == 400:
                    pass
                elif data['response'] == 401:
                    pass
                elif data['response'] == 402:
                    pass
                elif data['response'] == 403:
                    pass
                elif data['response'] == 404:
                    pass
                elif data['response'] == 409:
                    print(data['error'])
                    data = self.create_user_name()
                elif data['response'] == 410:
                    pass
                elif data['response'] == 500:
                    pass

            data['time'] = time.ctime(time.time())
            return data

    def service_msg(self):
        message = {'action': 'presence',
                   'type': 'status',
                   'user': {
                        'account_name': self.account_name,
                        'status': 'online'
                        }
                   }
        return message

    def auth_user(self):
        data = {'action': 'authenticate',
                'user': {
                    'account_name': self.account_name,
                    'password': self.password
                }
                }
        return data

    def user_to_user(self, data=None):
        if data is not None:
            print('From {}'.format(data['from']))
            print('Message: {}'.format(data['message']))
        send_to = input('To: ')
        message = input('Message: ')
        data = {
            'action': 'msg',
            'to': send_to,
            'from': self.account_name,
            'encoding': 'utf-8',
            'message': message
        }
        return data

    def user_to_chat(self, data=None):
        if data is not None:
            print('From {}'.format(data['from']))
            print('Message: {}'.format(data['message']))
        send_to = input('To: ')
        message = input('Message: ')
        data = {
            'action': 'msg',
            'to': '#' + send_to,
            'from': self.account_name,
            'encoding': 'utf-8',
            'message': message
        }
        return data

    def quit(self):
        data = {'action': 'quit',
                'account_name': self.account_name}
        return data

def main():
    data = cl_client_options()
    if isinstance(data, dict):
        with socket.create_connection((data['addr'], data['port'])) as sock:
            user = Client()
            user.create_user_name()
            while True:
                data_msg = get_msg(sock)
                data_msg = user.client_response(data_msg)
                if 'action' in data_msg:
                    if data_msg['action'] == 'quit':
                        break
                send_msg(sock, data_msg)
    else:
        for i in data:
            print(i)


if __name__ == '__main__':
    main()

