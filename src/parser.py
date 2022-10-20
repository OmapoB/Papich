import re
import pandas as pd
import pathlib as pl
from MyLibs.data_loader import DataFrameLoader

path_from = pl.Path('../data/Prays-list_21_08_2022.xls')
path_to = pl.Path('../data/stocks_2.xlsx')

file_from = DataFrameLoader(path='../data/Prays-list_21_08_2022.xls',
                            cols=['Номенклатура',
                                  'Описание',
                                  'Ед.изм.',
                                  'Базовая',
                                  'Всего в наличии',
                                  'Заказать',
                                  'Региональный склад',
                                  'Витрина ОК Галерея Кухни'],
                            skip=2).load_df().astype({'Код для поиска': 'int32'})

file_to = DataFrameLoader(path='../data/stocks_2.xlsx',
                          cols=['Баркод',
                                'Вид товара',
                                'Бренд',
                                'Наименование',
                                'Размер'],
                          skip=0).load_df()

searching = file_to['Артикул поставщика']

patterns_dict = {
    r'^([A-Za-z]+)(\d{3})\D+': [-1],
    r'.*(\d{5}).*(\1)': [5],
    r'.*(\d{4}).*(\1)': [4],
    r'.*(\d{3}).*(\1)': [3],
    r'.*(\d{5})$': [-1]
}

codes_dict = {}


def true_code_finder(raw_string, supposed_code):
    code = re.search(r'\D+(\d{3,5}$)', raw_string)
    if code is not None:
        codes_dict.update({raw_string: code.groups()[-1]})
    else:
        codes_dict.update({raw_string: supposed_code})


def find_by_pattern(pattern, where):
    to_delete = []
    for j in range(len(where)):
        find = re.search(pattern, where[j])
        if find is not None:
            patterns_dict[pattern].append(where[j])
            to_delete.append(j)
            match patterns_dict[pattern][0]:
                case 5:
                    codes_dict.update({where[j]: find.groups()[-1]})
                case 4:
                    true_code_finder(where[j], find.groups()[-1])
                case 3:
                    true_code_finder(where[j], find.groups()[-1])

    where.drop(to_delete, axis=0, inplace=True)
    where.reset_index(drop=True, inplace=True)
    return where


for key in patterns_dict.keys():
    searching = find_by_pattern(key, searching)

for item in codes_dict.items():
    print(item)
# for k, item in enumerate(codes_dict.items(), 1):
#     print(k, ' ', item)

# finder = re.search(r'.*(\d{5}).*(\1)', searching[0])
# print(finder.groups()[-1])


# for item in patterns_dict.items():
#     for i in item[1]:
#         print(i)
#     print()
# в начале
# ^([A-z]*)(\d{3})

# в потом
# .*(\d{5}).*(\1)
# .*(\d{4}).*(\1) если с конца больше 4 чисел то берем это число
# .*(\d{3}).*(\1)
# .*(\d{2}).*(\1)
# .*(\d{1}).*(\1)

# в конце
# .*(\d{5})$
