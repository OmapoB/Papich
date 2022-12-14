import re
import pathlib as pl

import pandas as pd
from numpy import int32

from MyLibs.data_loader import DataFrameLoader
from MyLibs.GUI import *


def main():
    path_to = pl.Path(main_window.get_input_to())

    to_change = pd.read_excel(path_to)

    file_from = DataFrameLoader(cols=['Номенклатура',
                                      'Описание',
                                      'Ед.изм.',
                                      'Базовая',
                                      'Всего в наличии',
                                      'Заказать',
                                      'Региональный склад',
                                      'Витрина ОК Галерея Кухни'],
                                skip=2)
    file_from.set_path(main_window.get_input_from())
    file_from = file_from.load_df()
    file_from = file_from.astype({'Код для поиска': 'int32'})

    file_to = DataFrameLoader(cols=['Баркод',
                                    'Вид товара',
                                    'Бренд',
                                    'Наименование',
                                    'Размер'],
                              skip=0)
    file_to.set_path(main_window.get_input_to())
    file_to = file_to.load_df()

    searching = file_to['Артикул поставщика']

    patterns_dict = {
        r'^([A-Za-z]+)(\d{3})\D+': [-1],
        r'.*(\d{5}).*(\1)': [5],
        r'.*(\d{4}).*(\1)': [4],
        r'.*(\d{3}).*(\1)': [3],
        r'.*(\d{2}).*(\1)': [2],
        r'.*(\d{1}).*(\1)': [1],
        r'.*(\d{5})$': [-1]
    }

    codes_dict = {}

    def true_code_finder(raw_string, supposed_code):
        code = re.search(r'\D+(\d{1,5}$)', raw_string)
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
                    case 2:
                        true_code_finder(where[j], find.groups()[-1])
                    case 1:
                        true_code_finder(where[j], find.groups()[-1])
                    case -1:
                        codes_dict.update({where[j]: find.groups()[-1]})

        where.drop(to_delete, axis=0, inplace=True)
        where.reset_index(drop=True, inplace=True)
        return where

    for key in patterns_dict.keys():
        searching = find_by_pattern(key, searching)

    errors = {'Артикул поставщика': [],
              'Найденный код': []}

    file_from.set_index('Код для поиска', inplace=True)
    to_change.set_index('Артикул поставщика', inplace=True)

    for raw_code, code in codes_dict.items():
        try:
            amount = file_from.loc[int32(code)]
            try:
                if int(amount) in range(0, 3):
                    amount = 0
                else:
                    amount = int(amount // 2)
            except ValueError as e:
                amount = 0
            finally:
                to_change.loc[[raw_code], ['Количество']] = amount
        except KeyError:
            errors['Артикул поставщика'].append(raw_code)
            errors['Найденный код'].append(code)

    to_change.reset_index(inplace=True)
    to_change = to_change.reindex(columns=['Баркод',
                                           'Количество',
                                           'Вид товара',
                                           'Бренд',
                                           'Наименование',
                                           'Размер',
                                           'Артикул поставщика'])
    output_save = pd.ExcelWriter('123.xlsx')
    to_change.to_excel(output_save)
    output_save.save()
    errors = pd.DataFrame(errors)
    errors_save = pd.ExcelWriter('Errors.xlsx')
    errors.to_excel(errors_save)
    errors_save.save()


if __name__ == '__main__':
    root = Tk()
    main_window = MainWindow(root)
    main_window.submit.config(command=main)
    root.mainloop()
