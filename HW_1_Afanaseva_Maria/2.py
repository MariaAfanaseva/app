"""

2. Каждое из слов «class», «function»,
«method» записать в байтовом типе без преобразования
в последовательность кодов (не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

"""

word_1 = b'class'
word_2 = b'function'
word_3 = b'method'
print(type(word_1))
print(type(word_2))
print(type(word_3))
print(word_1)
print(word_2)
print(word_3)
print(len(word_1))
print(len(word_2))
print(len(word_3))
