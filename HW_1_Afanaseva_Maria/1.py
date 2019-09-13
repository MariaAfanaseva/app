"""

1. Каждое из слов «разработка», «сокет»,
«декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые
представление в формат Unicode и также проверить тип и содержимое переменных.

"""

word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'
print(type(word_1))
print(type(word_2))
print(type(word_3))
print(word_1)
print(word_2)
print(word_3)

development = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
socket = '\u0441\u043e\u043a\u0435\u0442'
decorator = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
print(type(development))
print(type(socket))
print(type(decorator))
print(development)
print(socket)
print(decorator)
