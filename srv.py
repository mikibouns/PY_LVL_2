import socket
import threading

from secondary_func import cl_options, get_msg, send_msg
from data_base import DataBase
from decorators import log

db = DataBase()


class context_mgr:
    def __init__(self, current_chat):
        self.current_chat = current_chat

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass



class Srv:
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
            chat_control = ChatController(self, conn, self.account_name)
            th = threading.Thread(target=self.handle_client, args=(chat_control, ))
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

    def handle_client(self, chat_control):
            try:
                while chat_control.chats_controller_menu():
                    chat_control.join_chat()
            except ConnectionResetError:
                self.delete_client()

    def delete_client(self):
        try:
            self.account_name = db.clients_list.pop(self.account_name)
        except Exception as e:
            print(e)
        else:
            print('disconnected client: {}:{}'.format(self.addr[0], self.addr[1]))
            return self.account_name


class ChatController:
    def __init__(self, srv, conn, account_name):
        self.srv = srv
        self.conn = conn
        self.account_name = account_name
        self.current_chat = None

    def chats_controller_menu(self):
        while True:
            data = get_msg(self.conn)

            if data['action'] == 'chats_list':
                chats_list = [str(i) for i in db.chats_list.keys()]
                chats_list.sort()
                send_msg(self.conn, chats_list)
            elif data['action'] == 'add_chat':
                self.current_chat = data['msg']
                if self.current_chat not in db.chats_list:
                    self.add_chat(self.current_chat)
                    self.conn.send(b'200')
                    return True
                else:
                    self.conn.send(b'404')
            elif data['action'] == 'join_chat':
                self.current_chat = data['msg']
                if self.current_chat in db.chats_list:
                    self.conn.send(b'200')
                    return True
                else:
                    self.conn.send(b'404')
            elif data['action'] == 'quit':
                self.srv.delete_client()
                self.conn.send(b'quit')
                return False

    def add_chat(self, chat_name):
        try:
            chat = Chat()
            db.chats_list[chat_name] = chat
        except Exception as e:
            print(e)

    def join_chat(self):
        db.chats_list[self.current_chat].add_to_chat(self.conn, self.account_name)
        chat = db.chats_list[self.current_chat]
        client = db.clients_list[self.account_name]
        while True:
            try:
                data = client.recv(1024).decode(self.srv.encoding)
                if data == 'quit':
                    self.leave_chat(self.current_chat)
                    break
                else:
                    data = '{}: {}'.format(self.account_name, data)
                    chat.broadcast_request(data)
            except ConnectionResetError:
                self.leave_chat(self.current_chat)
                raise ConnectionResetError

    def leave_chat(self, chat):
        print('user {} left "{}" chat!'.format(self.account_name, chat))
        try:
            db.chats_list[self.current_chat].users.pop(self.account_name)
            self.conn.send(b'quit')
        except Exception as e:
            print(e)


class Chat:
    def __init__(self):
        self.users = {}
        self.encoding = 'utf-8'
        self.chat_history = []

    def add_to_chat(self, conn, account_name):
        self.users[account_name] = conn
        data = 'user {} joined "{}" chat!'.format(account_name, )
        print(data)
        self.chat_history.append(data)

    def broadcast_request(self, data):
        if self.users:
            print(data)
            for client in self.users.values():
                client.send(data.encode(self.encoding))




def main():
    with socket.socket() as sock:
        srv = Srv(sock)
        srv.run_srv()



if __name__ == '__main__':
    chat1 = Chat()
    chat2 = Chat()
    db.chats_list['chat1'] = chat1
    db.chats_list['chat2'] = chat2
    main()


