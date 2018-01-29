from subprocess import call
import os
import re

def gen_test_list():
    for i in os.listdir(os.getcwd()):
        if re.match(r'test', i):
            print(i)
            yield i

if __name__ == '__main__':
    for i in gen_test_list():
        test_cmd = 'pytest -s -v {}'.format(i)
        call(test_cmd, shell=True)