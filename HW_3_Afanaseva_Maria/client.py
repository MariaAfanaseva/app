import sys
import time
import re
import socket
from common.variables import *
from common.utils import *


#  обрабатываем аргументы
def get_ip_port():
    try:
        ip_server = sys.argv[1]
        port_server = int(sys.argv[2])
        if not 1024 < port_server < 65535 or not \
                re.match(r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)'
                         r'{3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', ip_server):
            raise ValueError
    except IndexError:
        ip_server = DEFAULT_IP_ADDRESS
        port_server = DEFAULT_PORT
    except ValueError:
        print('Неверный ip или port (1024 - 65535)')
        exit(1)
    return ip_server, port_server


def create_presence_msg(account_name='Guest'):
    try:
        if not isinstance(account_name, str) or len(account_name) > 25:
            raise SyntaxError(account_name)
    except SyntaxError:
        print('Имя должно быть словом не длиннее 25')
        exit(1)
    msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return msg


def valid_server_answer(msg):
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            return 'OK: 200'
        elif msg[RESPONSE] == 400:
            return f'400 : {msg[ERROR]}'
    raise ValueError


def main():
    contact = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    contact.connect((get_ip_port()))
    msg_to_server = create_presence_msg()
    send_msg(contact, msg_to_server)
    print(valid_server_answer(get_msg(contact)))


if __name__ == '__main__':
    main()
