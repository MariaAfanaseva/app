import socket
import sys
import re
from common.variables import *
from common.utils import *


def get_addr_port():
    args = sys.argv
    try:
        if '-a' in args:
            address = args[args.index('-a') + 1]
        else:
            address = ''
    except IndexError:
        print('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        exit(1)
    try:
        if '-p' in args:
            port = int(args[args.index('-p') + 1])
        else:
            port = DEFAULT_PORT
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        exit(1)
    try:
        if address and not re.match(r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)'
                        r'{3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', address) or not 1024 < port < 65535:
            raise ValueError
    except ValueError:
        print('Неверные значения port (-p) или ip (-a)')
        exit(1)
    return address, port


def valid_client_msg(message):
    if ACTION in message and TIME in message and USER in message and message[ACTION] == PRESENCE:
        return {RESPONSE: 200}
    else:
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }


def main():
    contact = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Готовим сокет
    contact.bind(get_addr_port())
    contact.listen(MAX_CONNECTIONS)  # Слушаем порт
    while True:
        client, client_address = contact.accept()
        message = get_msg(client)
        print(message)
        response = valid_client_msg(message)
        send_msg(client, response)
        client.close()


if __name__ == '__main__':
    main()
