import socket
import sys
import re
import logging
import argparse
import select
import time
from common.variables import *
from common.utils import *
from logs import server_log_config
from  common.errors import IncorrectDataNotDictError
from decorators.decos import Decoration

logger = logging.getLogger('server')
logger.setLevel(logging.INFO)


@Decoration()
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int)
    parser.add_argument('-a', '--addr', default='')
    names = parser.parse_args(sys.argv[1:])
    address = names.addr
    port = names.port

    if address and not re.match(r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)'
                    r'{3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', address) or not 1024 < port < 65535:
        print('Неверные значения port (-p) или ip (-a)')
        logger.critical('Неверные значения port (-p) или ip (-a)')
        exit(1)
    logger.info(f'Полученны данные ip и port, которые слушает сервер - {address}, {port}')

    return address, port


@Decoration()
def client_msg(message, messages, client):
    logger.debug(f'Разбор сообщения от клиента - {message}')
    if ACTION in message and TIME in message and USER in message and message[ACTION] == PRESENCE:
        msg = {RESPONSE: 200}
        send_msg(client, msg)
        logger.debug(f'Отправлен ответ клиенту - {msg} \n')
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        messages.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
    else:
        msg = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        send_msg(client, msg)
        logger.info(f'Отправлен ошибки клиенту - {msg} \n')


@Decoration()
def send_message(clients_send_lst, messages):
    if messages and clients_send_lst:
        msg = {
            ACTION: MESSAGE,
            FROM: messages[0][0],
            TIME: time.time(),
            MESSAGE_TEXT: messages[0][1]
        }
        del messages[0]
        for client in clients_send_lst:
            try:
                send_msg(client, msg)
            except ConnectionResetError:
                logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
                client.close()
                clients.remove(client)


@Decoration()
def main():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Готовим сокет
    connection.bind(get_args())
    connection.settimeout(0.5)
    connection.listen(MAX_CONNECTIONS)  # Слушаем порт

    clients = []
    messages = []

    while True:
        try:
            client, client_address = connection.accept()
        except OSError:
            pass
        else:
            logger.info(f'Установлено соединение с клиетом - {client_address}')
            clients.append(client)

        clients_read_lst = []
        clients_send_lst = []
        err_lst = []

        try:
            if clients:
                clients_read_lst, clients_send_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if clients_read_lst:
            for client in clients_read_lst:
                try:
                    client_msg(get_msg(client), messages, client)
                    logger.debug('Получено сообщение от клиента')
                except IncorrectDataNotDictError:
                    logger.error('Получен не верный формат данных')
                except ConnectionResetError:
                    logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
                    client.close()
                    clients.remove(client)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        send_message(clients_send_lst, messages)


if __name__ == '__main__':
    main()
