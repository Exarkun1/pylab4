import yfinance as yf
import pandas as pd
from pandas import DataFrame, Series, ExcelWriter
from datetime import datetime, timedelta

class DataStorage:
    '''
    Класс для взаимодейтсвия с данными
    '''
    def __init__(self,
                 path: str):
        self.__path = path


    def save(self,
             data: DataFrame,
             sheet: str):
        '''
        Метод сохраняющий временные ряды в эксель таблицу
        Args:
            data: Датафрейм для сохранения в эксель
            sheet: Название листа в которой будет создана таблица
        '''
        with ExcelWriter(self.__path, mode='a', if_sheet_exists='replace') as writer:
            data.to_excel(writer, sheet_name=sheet)


    def load(self,
             sheet: str,
             index_col: str) -> DataFrame:
        '''
        Метод выгружающий данные из эксель таблицы

        Args:
             sheet: название листа с которого будет взята таблица
             index_col: номер стобца таблицы

        Returns:
            Таблица с временными рядами
        '''
        return pd.read_excel(self.__path, sheet_name=sheet, index_col=index_col)


if __name__ == "__main__":
    pass
