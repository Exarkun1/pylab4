import numpy as np
import pandas as pd
from pandas import DataFrame

import utils
from data_storage import DataStorage
from plots import Drawer

def is_exit(comand: list[str]) -> bool:
    return len(comand) == 1 and comand[0] == "exit"

def is_load(comand: list[str]) -> bool:
    return len(comand) == 2 and comand[0] == "load"

def is_save(comand: list[str]) -> bool:
    return len(comand) == 2 and comand[0] == "save"

def is_download(comand: list[str]) -> bool:
    return len(comand) == 5 and comand[0] == "download"

def is_draw(comand: list[str]) -> bool:
    return len(comand) == 1 and comand[0] == "draw"

if __name__ == "__main__":
    path = "Storage.xlsx"
    storage = DataStorage(path)
    drawer = Drawer()

    df = None

    while(True):
        comand = utils.comand_to_list(input())
        if is_exit(comand):
            break
        elif is_load(comand):
            df = storage.load(sheet=comand[1], index_col="Date")
            print(df)
        elif is_save(comand):
            storage.save(df, sheet=comand[1])
        elif is_download(comand):
            series = storage.download(org=comand[1],
                                  period=utils.str_to_timedelta(comand[2]),
                                  interval=comand[3])
            df = utils.calculate_dataframe(series=series, 
                                           interval=comand[3], 
                                           window=comand[4])
        elif is_draw(comand):
            drawer.plot(df)
        else:
            print("Не известная команда.")