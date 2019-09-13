"""

Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.

"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    data_dict = {
                 'item': item,
                 'quantity': quantity,
                 'price': price,
                 'buyer': buyer,
                 'date': date
                 }
    with open('orders.json', 'r', encoding='utf-8') as r_file:
        data = json.load(r_file)
        lst = data['orders']
        lst.append(data_dict)
    with open('orders.json', 'w', encoding='utf-8') as w_file:
        json.dump(data, w_file, indent=4)


write_order_to_json('Table', 1, 4566, 'Anna', '11.11.11')
