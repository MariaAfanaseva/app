"""

Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.

"""
import yaml


data = {
    'names': ['table', 'sofa', 'computer', 'lamp'],
    'quantity': 3,
    'price': {
        'table': '100€ - 200€',
        'sofa': '300€ - 500€',
        'computer': '500€ - 800€',
        'lamp': '200€'
    }
}

with open('file.yaml', 'w') as w_file:
    yaml.dump(data, w_file, allow_unicode=True, default_flow_style=False)
with open('file.yaml', 'r') as r_file:
    # print(yaml.load(r_file, Loader=yaml.FullLoader))
    print(r_file.read())
