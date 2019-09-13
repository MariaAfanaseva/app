"""

5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.

"""

import subprocess
import chardet


def ping_yandex():
    args = ['ping', 'yandex.ru']
    ya_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in ya_ping.stdout:
        # print(line)
        result = chardet.detect(line)
        # print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


def ping_youtube():
    args = ['ping', 'youtube.com']
    youtube_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line_bytes in youtube_ping.stdout:
        # print(line_bytes)
        coding = chardet.detect(line_bytes)
        # print(coding)
        line_bytes = line_bytes.decode(coding['encoding']).encode('utf-8')
        line_str = line_bytes.decode('utf-8')
        print(line_str)


ping_yandex()
ping_youtube()
