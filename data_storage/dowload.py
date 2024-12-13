import yfinance as yf
from datetime import datetime, timedelta
from pandas import Series


class Downloader:
    def download(self,
                 org: str,
                 period: timedelta,
                 interval: str) -> Series:
        """
        Метод для загрузки данных из интернета

        Args:
            org: Название ценных бумаг для выгрузки
            period: Рассматриваемый период
            interval: Интервал для загрузки данных

        Returns:
            Временной ряд
        """
        data = yf.download(tickers=org,
                           start=(datetime.now()-period),
                           interval=interval)
        values = data["Open"].values
        values = values.reshape(values.shape[0])
        return Series(values, index=data.index)


if __name__ == "__main__":
    pass
