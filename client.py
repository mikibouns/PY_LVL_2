from contextlib import contextmanager
import socket
import time

from secondary_func import cl_client_options, get_msg, send_msg


class Client:
    def __init__(self):
        self.account_name = None
        self.password = None

    def menu(self):
        while True:
            print('''
        ##################### MAIN MENU ######################
        1. Log in
        2. Log in as guest
        3. To register
        4. Quit
        ######################################################
                ''')
            data = input('Enter the number of menu: ')
            if not data.isdigit():
                continue
            elif data == '1':
                return self._login()
            elif data == '2':
                return self._login_as_guest()
            elif data == '3':
                print('REGISTER')
            elif data == '4':
                return self.quit()

    def messenger_menu(self):
        while True:
            print('''
        ################### MESSENGER MENU ###################
        1. User to user
        2. User to chat
        3. Back to menu
        4. Quit
        ######################################################
                    ''')
            data = input('Enter the number of menu: ')
            if not data.isdigit():
                continue
            elif data == '1':
                pass
            elif data == '2':
                pass
            elif data == '3':
                return self.menu()
            elif data == '4':
                return self.quit()

    def client_response(self, data):
        if isinstance(data, dict):
            if 'action' in data:
                if data['action'] == 'probe':
                    data = self.menu()
                elif data['action'] == 'msg' and data['to'][0] == '#':
                    data = self.user_to_chat()
                elif data['action'] == 'msg':
                    data = self.user_to_user()

            elif 'response' in data:
                if data['response'] == 200:
                    data = self.messenger_menu()
                elif data['response'] == 201:
                    pass
                elif data['response'] == 202:
                    pass
                elif data['response'] == 400:
                    pass
                elif data['response'] == 401:
                    pass
                elif data['response'] == 402:
                    print(data['error'])
                    data = self.menu()
                elif data['response'] == 403:
                    pass
                elif data['response'] == 404:
                    pass
                elif data['response'] == 409:
                    print(data['error'])
                    data = self.menu()
                elif data['response'] == 410:
                    pass
                elif data['response'] == 500:
                    pass

            data['time'] = time.ctime(time.time())
            return data

    def _login_as_guest(self):
        while True:
            self.account_name = input('Enter your username: ')
            if len(self.account_name) < 25:
                return self.service_msg()
            else:
                print('Please enter a username of up to 25 characters!!!')

    def _login(self):
        while True:
            self.account_name = input('Enter your username: ')
            self.password = input('Enter your password: ')
            if len(self.account_name) < 25:
                return self.auth_user()
            else:
                print('Please enter a username of up to 25 characters!!!')

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
                'account_name': self.account_name,
                'time': time.ctime(time.time())}
        return data


def main():
    data = cl_client_options()
    if isinstance(data, dict):
        with socket.create_connection((data['addr'], data['port'])) as sock:
            user = Client()
            while True:
                data_msg = get_msg(sock)
                print(data_msg)
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

