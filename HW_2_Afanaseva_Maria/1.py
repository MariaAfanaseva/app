"""

1. Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных
данных из файлов info_1.txt, info_2.txt, info_3.txt и
формирующий новый «отчетный» файл в формате CSV.

"""
import csv
import re


def get_data():
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for i in range(1, 4):
        with open(f'info_{i}.txt', 'r', encoding='cp1251') as file:
            # print(file.read())
            for line in file:
                line_re = re.match(r'Изготовитель системы|Название ОС|Код продукта|Тип системы', line)
                if line_re:
                    line = line.strip().split(':')
                    if line[0] == 'Изготовитель системы':
                        os_prod_list.append(line[1].lstrip())
                    elif line[0] == 'Название ОС':
                        os_name_list.append(line[1].lstrip())
                    elif line[0] == 'Код продукта':
                        os_code_list.append(line[1].lstrip())
                    elif line[0] == 'Тип системы':
                        os_type_list.append(line[1].lstrip())
    for i in range(3):
        main_data.append([])
        main_data[i + 1].append(os_prod_list[i])
        main_data[i + 1].append(os_name_list[i])
        main_data[i + 1].append(os_code_list[i])
        main_data[i + 1].append(os_type_list[i])
    return main_data


def write_to_csv():
    data = get_data()
    # print(data)
    with open('report.csv', 'w', encoding='utf-8', newline='') as file:
        file_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        file_writer.writerows(data)


def print_csv():
    with open('report.csv', 'r', encoding='utf-8') as file:
        file_reader = csv.reader(file)
        print(list(file_reader))


write_to_csv()
print_csv()
