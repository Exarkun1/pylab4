import yfinance as yf
import pandas as pd
from pandas import DataFrame, Series, ExcelWriter
from datetime import datetime, timedelta

class DataStorage:
    def __init__(self,
                 path: str):
        self.__path = path


    def save(self,
             data: DataFrame,
             sheet: str):
        with ExcelWriter(self.__path, mode='a', if_sheet_exists='replace') as writer:
            data.to_excel(writer, sheet_name=sheet)


    def load(self,
             sheet: str,
             index_col: str) -> DataFrame:
        return pd.read_excel(self.__path, sheet_name=sheet, index_col=index_col)


    def download(self,
                 org: str,
                 period: timedelta,
                 interval: timedelta) -> Series:
        data = yf.download(tickers=org, 
                           start=(datetime.now()-period),
                           interval=interval)
        values = data["Open"].values
        values = values.reshape(values.shape[0])
        return Series(values, index=data.index)