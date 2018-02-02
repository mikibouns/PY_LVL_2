import socket
import time

from secondary_func import cl_client_options, get_msg, send_msg


class Client:
    def __init__(self):
        self.account_name = None
        self.password = None
        self.room = None
        self.to_user = None
        self._quit = {'action': 'quit',
                     'account_name': self.account_name,
                     'time': time.ctime(time.time())}


    def client_response(self, data):
        if isinstance(data, dict):
            if 'action' in data:
                if data['action'] == 'probe':
                    data = self.presence_msg()

            elif 'response' in data:
                if data['response'] == 200:
                    pass
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
                    return self.auth_user()
                elif data['response'] == 403:
                    print(data['error'])
                elif data['response'] == 404:
                    print(data['error'])
                elif data['response'] == 409:
                    print(data['error'])
                    return self.main_menu()
                elif data['response'] == 410:
                    print(data['error'])
                elif data['response'] == 500:
                    print(data['error'])

            data['time'] = time.ctime(time.time())
            return data


    def main_menu(self):
        while True:
            print('''
        ##################### MAIN MENU ######################
        1. Log in
        2. Quit
        ######################################################
                ''')
            data = input('Enter the number of menu: ')
            if not data.isdigit():
                continue
            elif data == '1':
                return self.login()
            elif data == '2':
                return self._quit


    def login(self):
        while True:
            self.account_name = input('Enter your username: ')
            if len(self.account_name) < 25:
                return self.presence_msg()
            else:
                print('Please enter a username of up to 25 characters!!!')


    def presence_msg(self):
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


    def _send_message(self, data=None):
        if data is not None:
            print('From {}'.format(data['from']))
            print('Message: {}'.format(data['message']))
        message = input('Message: ')
        return message


    def user_to_user(self, data=None):
        message = self._send_message(data)
        data = {
            'action': 'msg',
            'to': self.to_user,
            'from': self.account_name,
            'encoding': 'utf-8',
            'message': message
        }
        return data


    def user_to_chat(self, data=None):
        message = self._send_message(data)
        data = {
            'action': 'msg',
            'to': '#{}'.format(self.room),
            'from': self.account_name,
            'encoding': 'utf-8',
            'message': message
        }
        return data


    def join_chat(self):
        self.room = input('Join chat: ')
        response = {
            'action': 'join',
            'room': '#{}'.format(self.room)
        }
        return response


    def leave_chat(self):
        response = {
            'action': 'leave',
            'room': '#{}'.format(self.room)
        }
        return response


def main():
    data = cl_client_options()
    if isinstance(data, dict):
        with socket.create_connection((data['addr'], data['port'])) as sock:
            user = Client()
            send_msg(sock, user.main_menu())
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

