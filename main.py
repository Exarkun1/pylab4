import numpy as np
import pandas as pd
from pandas import DataFrame

import utils
from data_storage import DataStorage
from plots import Drawer

def is_exit(command: list[str]) -> bool:
    return len(command) >= 1 and command[0] == "exit"

def is_load(command: list[str]) -> bool:
    return len(command) == 2 and command[0] == "load"

def is_save(command: list[str]) -> bool:
    return len(command) == 2 and command[0] == "save"

def is_download(command: list[str]) -> bool:
    return len(command) == 5 and command[0] == "download"

def is_draw(command: list[str]) -> bool:
    return len(command) > 1 and command[0] == "draw"

def is_help(command: list[str]) -> bool:
    return len(command) == 1 and command[0] == "help"

if __name__ == "__main__":
    path = "Storage.xlsx"
    storage = DataStorage(path)
    drawer = Drawer()

    df = None
    
    print("Программа запущена. Введите help для получения списка команд программы.")

    while(True):
        command = utils.command_to_list(input())
        if is_exit(command):
            break
        elif is_load(command):
            df = storage.load(sheet=command[1], index_col="Date")
            print(df)
        elif is_save(command):
            storage.save(df, sheet=command[1])
        elif is_download(command):
            series = storage.download(org=command[1],
                                  period=utils.str_to_timedelta(command[2]),
                                  interval=command[3])
            df = utils.calculate_dataframe(series=series, 
                                           interval=command[3], 
                                           window=command[4])
        elif is_draw(command):
            drawer.plot(df, command[1:])
        elif is_help(command):
            print("Список команд:")
            print("exit - завершить программу.")
            print("load [sheet name] - загрузить страницу [sheet name] из .xslx файла.")
            print("save [sheet name] - сохранить данные в страницу [sheet name] .xslx файла.")
            print("download [organization] [period] [interval] [window] - загружает данные указанно компании за указанный интервал с определенным периодом." + 
                "Вычисляет все данные с указанным окном скользящего среднего.")
            print("draw - Отобразить графики рассчитанных значений.")

        else:
            print("Не известная команда.")