import socket

from secondary_func import cl_options

def send_msg(sock, text):
    msg = input(text).encode('utf-8')
    sock.send(msg)


def get_msg(sock):
    data = sock.recv(1024)
    return data.decode('utf-8')


def main():
    addr = cl_options()
    with socket.socket() as sock:
        sock.connect((addr['addr'], addr['port']))
        while True:
            send_msg(sock, 'Enter your account name: ')
            data = get_msg(sock)
            if data == '409':
                print('account name already exists!')
            while data == '200':
                print(get_msg(sock))



if __name__ == '__main__':
    main()