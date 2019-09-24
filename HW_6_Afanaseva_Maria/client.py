import sys
import time
import re
import socket
import logging
from common.variables import *
from common.utils import *
from logs import client_log_config
from common.errors import IncorrectDataNotDictError, FieldMissingError, IncorrectCodeError
from common.decos import Decoration

#  логирование в журнал
logger = logging.getLogger('client')
logger.setLevel(logging.DEBUG)


#  обрабатываем аргументы
@Decoration()
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
        logger.critical(f'Неверный ip или port (1024 - 65535) - {ip_server}, {port_server}\n')
        exit(1)
    logger.info(f'Полученны данны ip и port сервера - {ip_server}, {port_server}')
    return ip_server, port_server


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
def main():
    contact = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        contact.connect((get_ip_port()))
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
        print(answer)
    except IncorrectDataNotDictError:
        logger.error('Получен не верный формат данных\n')
    except FieldMissingError as missing_error:
        logger.error(f'Нет обязательного поля - {missing_error}\n')
    except IncorrectCodeError as wrong_code:
        logger.error(f'Неверный код в сообщении - {wrong_code}')


if __name__ == '__main__':
    main()
