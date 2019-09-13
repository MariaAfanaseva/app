"""

3. Определить, какие из
слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе.

"""

words = ['attribute', 'класс', 'функция', 'type']
print('Невозможно записать в байтовом типе в кодировке ascii слова:', end=' ')
for word in words:
    try:
        word.encode('ascii')
    except ValueError:
        print(word, end=' ')
