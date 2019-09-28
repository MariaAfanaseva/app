import sys
import time
import re
import socket
import logging
import argparse
import json
from common.variables import *
from common.utils import *
from logs import client_log_config
from common.errors import IncorrectDataNotDictError, FieldMissingError, IncorrectCodeError
from decorators.decos import Decoration

#  логирование в журнал
logger = logging.getLogger('client')
logger.setLevel(logging.DEBUG)


#  обрабатываем аргументы
@Decoration()
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    names = parser.parse_args(sys.argv[1:])
    ip_server = names.ip
    port_server = names.port
    mode_client = names.mode

    if not 1024 < port_server < 65535 or not \
            re.match(r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)'
                     r'{3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', ip_server):
        # print(f'Неверный ip или port (1024 - 65535) - {ip_server}, {port_server}')
        logger.critical(f'Неверный ip или port (1024 - 65535) - {ip_server}, {port_server}\n')
        exit(1)
    logger.info(f'Полученны данны ip и port сервера - {ip_server}, {port_server}')

    if mode_client not in ('listen', 'send'):
        # print('Указан неверный режим работы. Допустимые: listen, send')
        logger.critical('Указан неверный режим работы. Допустимые: listen, send')
        exit(1)

    return ip_server, port_server, mode_client


@Decoration()
def create_presence_msg(account_name='Guest'):
    try:
        if not isinstance(account_name, str) or len(account_name) > 25:
            raise SyntaxError(account_name)
    except SyntaxError:
        logger.critical(f'Имя должно быть словом не длиннее 25 - {account_name}\n')
        exit(1)
    msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return msg


@Decoration()
def create_message(text, account_name='Guest'):
    try:
        if not isinstance(account_name, str) or len(account_name) > 25:
            raise SyntaxError(account_name)
    except SyntaxError:
        logger.critical(f'Имя должно быть словом не длиннее 25 - {account_name}\n')
        exit(1)
    message = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: text
    }
    logger.debug(f'Сформировано сообщение: {message}')
    return message


@Decoration()
def valid_server_answer(msg):
    logger.debug(f'Разбор сообщения от сервера - {msg}')
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            return 'OK: 200'
        elif msg[RESPONSE] == 400:
            return f'{msg[ERROR]}: 400'
        else:
            raise IncorrectCodeError(msg[RESPONSE])
    raise FieldMissingError(RESPONSE)


@Decoration()
def listen_message(message):
    if ACTION in message and message[ACTION] == MESSAGE and MESSAGE_TEXT in message and FROM in message:
        print(f'Получено сообщение от пользователя {message[FROM]}:\n{message[MESSAGE_TEXT]}')
        logger.info(f'Получено сообщение от пользователя {message[FROM]}:\n{message[MESSAGE_TEXT]}')
    else:
        logger.error(f'Получено некорректное сообщение с сервера: {message}')


@Decoration()
def chatter(sock, mode_client, ip_server):
    while True:
        try:
            if mode_client == 'send':
                text = input('Введите сообщение для отправки или "close" для завершения работы: ')
                if text == 'close':
                    sock.close()
                    logger.info('Завершение работы по команде пользователя.')
                    print('Спасибо за использование нашего сервиса!')
                    time.sleep(1)
                    exit(0)
                else:
                    send_msg(sock, create_message(text))
            elif mode_client == 'listen':
                listen_message(get_msg(sock))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            logger.error(f'Соединение с сервером {ip_server} было потеряно.')
            exit(1)


@Decoration()
def main():
    contact = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_server, port_server, mode_client = get_args()

    try:
        contact.connect((ip_server, port_server))
    except ConnectionRefusedError:
        logger.critical('Нелязя установить соединение. Не верные даннные ip или port\n')
        exit(1)

    logger.debug(f'Установлено соединение с сервером')
    msg_to_server = create_presence_msg()
    logger.info(f'Сформировано сообщение серверу - {msg_to_server}')
    send_msg(contact, msg_to_server)
    logger.debug(f'Отпавлено сообщение серверу')

    try:
        answer = valid_server_answer(get_msg(contact))
        logger.info(f'Получен ответ от сервера - {answer} \n')
        print(f'Установлено соединение с сервером')
    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')
        exit(1)
    except IncorrectDataNotDictError:
        logger.error('Получен не верный формат данных\n')
        exit(1)
    except FieldMissingError as missing_error:
        logger.error(f'Нет обязательного поля - {missing_error}\n')
        exit(1)
    except IncorrectCodeError as wrong_code:
        logger.error(f'Неверный код в сообщении - {wrong_code}')
        exit(1)
    except ConnectionResetError:
        logger.critical('Не установлена связь с сервером')
    else:
        if mode_client == 'send':
            print('Режим работы - отправка сообщений.')
        elif mode_client == 'listen':
            print('Режим работы - приём сообщений.')
        chatter(contact, mode_client, ip_server)


if __name__ == '__main__':
    main()
