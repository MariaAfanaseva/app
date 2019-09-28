import subprocess
import time


class Processes:
    def __init__(self, clients_listen, clients_send):
        self.clients_listen = clients_listen
        self.clients_send = clients_send

    def start_server_clients(self):
        processes = []
        while True:
            action = input('Введите нужную команду: \nstart - запустить сервер и клиентов,\n'
                           'close - закрыть все окна,\nexit - выход\n')
            if action == 'start':
                processes.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
                time.sleep(1)
                for _ in range(self.clients_listen):
                    processes.append(subprocess.Popen('python client.py -m listen', creationflags=subprocess.CREATE_NEW_CONSOLE))
                for _ in range(self.clients_send):
                    processes.append(subprocess.Popen('python client.py -m send', creationflags=subprocess.CREATE_NEW_CONSOLE))
            elif action == 'close':
                while processes:
                    client = processes.pop()
                    client.kill()
            elif action == 'exit':
                break


def main():
    processes = Processes(2, 2)
    processes.start_server_clients()


if __name__ == '__main__':
    main()
