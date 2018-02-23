import socket

from secondary_func import cl_options, get_msg, send_msg
from decorators import log

class Client:
    def __init__(self, sock):
        self.sock = sock
        self.user_name = ''
        self.password = ''
        self.encoding = 'utf-8'
        self.message = {'action': '',
                   'msg': ''}
        self.current_chat = None

    def run_client(self):
        while True:
            self.user_name = self.send_msg('Enter your account name: ')
            if self.user_name:
                data = self.get_msg()
                if data == '409':
                    print('account name already exists!')
                elif data == '200':
                    print('Welcome {}'.format(self.user_name.title()))
                    chat_control = ChatController(self.sock)
                    self.handle_request(chat_control)

    def handle_request(self, chat_control):
        while True:
            chat_control.chat_menu()
            chat_control.join_chat()

    def send_msg(self, text):
        msg = input(text).encode(self.encoding)
        if msg == '':
            return False
        self.sock.send(msg)
        return msg.decode(self.encoding)

    def get_msg(self):
        data = self.sock.recv(1024)
        return data.decode(self.encoding)


class ChatController(Client):
    def chat_menu(self):
        while True:
            print('''
    ----------- menu ----------
    1. chats list          
    2. join chat
    3. add chat                   
    4. quit                 
    ---------------------------
            ''')

            menu_item = input('enter the menu number: ')
            if menu_item == '1':
                self.message['action'] = 'chats_list'
                send_msg(self.sock, self.message)
                print('Chats list:')
                for chats in get_msg(self.sock):
                    print(chats)

            elif menu_item == '2':
                msg = input('please enter chat name: ')
                self.message['action'] = 'join_chat'
                self.message['msg'] = msg
                if msg:
                    send_msg(self.sock, self.message)
                    data = self.get_msg()
                    if data == '200':
                        break
                    elif data == '404':
                        print('user or chat is not on the server!')
                else:
                    print('input field is empty!')

            elif menu_item == '3':
                if self.add_chat():
                    break

            elif menu_item == '4':
                self.message['action'] = 'quit'
                send_msg(self.sock, self.message)
                if self.get_msg() == 'quit':
                    self.sock.close()
                    raise SystemExit(True)

    def join_chat(self):
        print('To leave the chat, send ==> quit')
        while True:
            if self.send_msg('>> '):
                msg = self.get_msg()
                if msg == 'quit':
                    break
                print(msg)

    def add_chat(self):
        data = input('please enter chat name: ')
        self.message['action'] = 'add_chat'
        if data:
            self.message['msg'] = data
            send_msg(self.sock, self.message)
            servise_response = self.get_msg()
            if servise_response == '200':
                print('chat created!')
                return True
            elif servise_response == '404':
                print('user or chat is not on the server!')
        else:
            print('input field is empty!')


def main():
    addr = cl_options()
    with socket.create_connection((addr['addr'], addr['port'])) as sock:
        client = Client(sock)
        client.run_client()


if __name__ == '__main__':
    main()

