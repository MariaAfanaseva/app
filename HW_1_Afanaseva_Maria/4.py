"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).

"""

words = ['разработка', 'администрирование', 'protocol', 'standard']
bytes_words = []
for word in words:
    word_bytes = word.encode('utf-8')
    bytes_words.append(word_bytes)
    print(f'{word} - {word_bytes}')

for word in bytes_words:
    word_str = word.decode('utf-8')
    print(f'{word} - {word_str}')
