import socket

from secondary_func import cl_options, get_msg, send_msg
from decorators import log

class Client:
    def __init__(self, sock):
        self.sock = sock
        self.user_name = ''
        self.password = ''
        self.encoding = 'utf-8'

    def run_client(self):
        while True:
            self.user_name = self.send_msg('Enter your account name: ')
            data = self.get_msg()
            if data == '409':
                print('account name already exists!')
            elif data == '200':
                print('Welcome {}'.format(self.user_name.title()))
                chat_control = ChatController(self.sock)
                while chat_control.chat_menu():
                    chat_control.join_chat()

                    self.send_msg('>> ')
                    msg = self.get_msg()
                    print(msg)

    def send_msg(self, text):
        msg = input(text).encode(self.encoding)
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
    3. quit                 
    ---------------------------
            ''')
            menu_item = input('enter the menu number: ')
            if menu_item == '1':
                self.sock.send(b'chats_list')
                print('Chats list:')
                for chats in get_msg(self.sock):
                    print(chats)
            elif menu_item == '2':
                self.sock.send(b'join_chat')
                self.send_msg('please enter the name of the chat: ')
                data = self.get_msg()
                if data == '200':
                    return True
                elif data == '404':
                    print('user or chat is not on the server')
            elif menu_item == '3':
                self.sock.send(b'quit')
                if self.get_msg() == 'quit':
                    self.sock.close()
                    raise SystemExit(True)

    def join_chat(self):
        print('Ok')

    def leave_chat(self):
        pass



def main():
    addr = cl_options()
    with socket.create_connection((addr['addr'], addr['port'])) as sock:
        client = Client(sock)
        client.run_client()




if __name__ == '__main__':
    main()

