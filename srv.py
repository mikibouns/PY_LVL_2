import socket
import threading

from secondary_func import cl_options, get_msg, send_msg
from data_base import DataBase
from decorators import log

db = DataBase()

class Srv:
    messages_list = []

    def __init__(self, sock):
        self.encoding = 'utf-8'
        a = cl_options()
        self.sock = sock
        self.sock.bind((a['addr'], a['port']))
        self.sock.listen(10)

    def run_srv(self):
        print('server is waiting for connection...')
        while True:
            conn, self.addr = self.sock.accept()
            print('connected client: {}:{}'.format(self.addr[0], self.addr[1]))
            self.account_name = self.check_account_data(conn)
            th = threading.Thread(target=self.handle_client, args=(conn, ))
            th.start()

    def check_account_data(self, conn):
        while True:
            self.account_name = conn.recv(1024).decode(self.encoding)
            if self.account_name in db.clients_list:
                conn.send(b'409')
            else:
                db.clients_list[self.account_name] = conn
                conn.send(b'200')
                break
        return self.account_name

    def handle_client(self, conn):
        try:
            chat_control = ChatController(self, conn)
            while chat_control.run_chats_controller():
                chat_control.join_chat()
                # data = conn.recv(1024).decode(self.encoding)
                # if not data:
                #     break
                # data = 'from {}: {}'.format(self.account_name, data)
                # print(data)
                # self._broadcast_request(data)
                pass
        except ConnectionResetError:
            self.delete_client()

    def _broadcast_request(self, data):
        for client in db.clients_list.values():
            client.send(data.encode(self.encoding ))

    def delete_client(self):
        try:
            self.account_name = db.clients_list.pop(self.account_name)
        except Exception as e:
            print(e)
            return False
        else:
            print('disconnected client: {}:{}'.format(self.addr[0], self.addr[1]))
            return self.account_name


class ChatController:
    def __init__(self, srv, conn):
        self.srv = srv
        self.conn = conn

    def run_chats_controller(self):
        while True:
            data = self.conn.recv(1024).decode(self.srv.encoding)
            if data == 'quit':
                self.srv.delete_client()
                self.conn.send(b'quit')
                return False
            elif data == 'chats_list':
                send_msg(self.conn, db.chats_list)
            elif data == 'join_chat':
                return True


    def add_chat(self):
        pass

    def join_chat(self):
        chat = self.conn.recv(1024).decode(self.srv.encoding)
        if chat in db.chats_list:
            self.conn.send(b'200')
            db.chats_list[chat].add_to_chat(self.conn)
            while True:
                db.chats_list[chat].broadcast_request(self.conn)
        else:
            self.conn.send(b'404')

    def leave_chat(self):
        pass



class Chat:
    def __init__(self):
        self.user = []
        self.encoding = 'utf-8'

    def add_to_chat(self, conn):
        self.user.append(conn)

    def broadcast_request(self, conn):
        data = conn.recv(1024).decode(self.encoding)
        print(data)
        for client in self.user:
            client.send(data.encode(self.encoding))

def main():
    with socket.socket() as sock:
        srv = Srv(sock)
        srv.run_srv()

if __name__ == '__main__':
    main()


