# Задание - 1
# Создайте функцию, принимающую на вход Имя, возраст и город проживания человека
# Функция должна возвращать строку вида "Василий, 21 год(а), проживает в городе Москва"


def about_user(name, age, city):
    return f'{name}, {age} год(а), проживает в городе {city}'


# Задание - 2
# Создайте функцию, принимающую на вход 3 числа, и возвращающую наибольшее из них


def max_function(a, b, c):
    max_number = a
    for num in [b, c]:
        if max_number < num:
            max_number = num
    return max_number


# Задание - 3
# Создайте функцию, принимающую неограниченное количество строковых аргументов,
# верните самую длинную строку из полученных аргументов


def long_str(*args):
    len_str = list(map(len, [*args]))
    len_str_zip = list(zip(len_str, [*args]))
    len_str_sort = sorted(len_str_zip, reverse=True)
    return len_str_sort[0][1]

    # or
    # return (max([*args], key=len))


def main():
    user = about_user('Maria', 21, 'Berlin')
    print(user)
    print(max_function(4, 23, 12))
    print(long_str('segd', 'Gzrzddg', 'aaa', 'zzz', 'srgshsshdf'))


if __name__ == '__main__':
    main()
