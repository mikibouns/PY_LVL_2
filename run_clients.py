from subprocess import Popen, CREATE_NEW_CONSOLE

p_list = []
num_clients = input('Enter number of clients: ')

while True:
    user = input('Run {} clients (s) / Close clients (x) / Quit (q): '.format(num_clients))
    if user == 'q':
        break
    elif user == 's':
        for name in range(int(num_clients)):
            p_list.append(Popen('python client.py', creationflags=CREATE_NEW_CONSOLE))
        print('{} clients launched'.format(num_clients))
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()