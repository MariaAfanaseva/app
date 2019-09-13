"""

6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

"""
import chardet

file = open('test.txt', 'w')
file.write('test')  # нельзя записать в файл кириллицу, ошибка кодировки
file.close()

with open('test.txt', 'r') as file:
    print(chardet.detect(file.read().encode())['encoding'])  # кодировка по умолчанию ASCII

with open('test_file.txt', 'w', encoding='utf-8') as file_1:
    # при явном указании кодировки можно записать в файл кириллицу
    file_1.write('сетевое программирование\nсокет\nдекоратор')
