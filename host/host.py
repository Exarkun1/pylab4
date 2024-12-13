from datetime import timedelta
from pandas import Series, DataFrame

from ui import UserInterface
from data_storage import DataStorage, Downloader
from time_series import TimeSeriesAnalyser


class Host:
    def __init__(self):
        self.ui = UserInterface()
        self.storage = DataStorage("Storage.xlsx")
        self.downloader = Downloader()

    def is_exit(self,
                command: list[str]) -> bool:
        '''
        Метод проверяющий что введена команда exit

        Args:
            command: Список аргументов
        Returns:
            Правильность формата bool
        '''
        return len(command) >= 1 and command[0] == "exit"

    def is_load(self,
                command: list[str]) -> bool:
        '''
        Метод проверяющий что введена команда load

        Args:
            command: Список аргументов
        Returns:
            Правильность формата bool
        '''
        return len(command) == 2 and command[0] == "load"

    def is_save(self,
                command: list[str]) -> bool:
        '''
        Метод проверяющий что введена команда save

        Args:
            command: Список аргументов
        Returns:
            Правильность формата bool
        '''
        return len(command) == 2 and command[0] == "save"

    def is_download(self,
                    command: list[str]) -> bool:
        '''
        Метод проверяющий что введена команда download

        Args:
            command: Список аргументов
        Returns:
            Правильность формата bool
        '''
        return len(command) == 5 and command[0] == "download"

    def is_draw(self,
                command: list[str]) -> bool:
        '''
        Метод проверяющий что введена команда draw

        Args:
            command: Список аргументов
        Returns:
            Правильность формата bool
        '''
        return len(command) > 1 and command[0] == "draw"

    def is_help(self,
                command: list[str]) -> bool:
        '''
        Метод проверяющий что введена команда help

        Args:
            command: Список аргументов
        Returns:
            Правильность формата bool
        '''
        return len(command) == 1 and command[0] == "help"

    def _str_to_timedelta(self,
                          period: str) -> timedelta:
        """
        Метод переводящий строку во временной период.

        Args:
            period: строковое представление временного периода.
        Returns:
            Временной период.
        """
        spl_period = period.split(",")
        seconds = 0
        for interval in spl_period:
            if interval[-1] == "s":
                seconds += int(interval[:-1])
            elif interval[-1] == "m":
                seconds += 60 * int(interval[:-1])
            elif interval[-1] == "h":
                seconds += 3600 * int(interval[:-1])
            elif interval[-1] == "d":
                seconds += 3600 * 24 * int(interval[:-1])
            elif interval[-1] == "w":
                seconds += 3600 * 24 * 7 * int(interval[:-1])
            elif interval[-2:] == "mo":
                seconds += 3600 * 24 * 30 * int(interval[:-2])
            elif interval[-1] == "y":
                seconds += 3600 * 24 * 365 * int(interval[:-1])
            else:
                raise RuntimeError("Неверный формат периода.")
        return timedelta(seconds=seconds)

    def _calculate_dataframe(self,
                             series: Series,
                             interval: str,
                             window: str) -> DataFrame:
        """
        Метод для вычисления временных рядов

        Args:
            series: Временной ряд
            interval: Интервал для дифференцирования
            window: окно для автокорреляции
        Returns:
            Таблица временных рядов
        """
        analyser = TimeSeriesAnalyser(series, self._str_to_timedelta(interval))
        movavg = analyser.calc_movavg(self._str_to_timedelta(window))
        analyser = TimeSeriesAnalyser(movavg, self._str_to_timedelta(interval))
        diff = analyser.differentiate()
        autocor = analyser.calc_autocor()
        return DataFrame({"Open": series, "Movavg": movavg, "Diff": diff, "Autocor": autocor})

    def start(self):
        df = None

        while(True):
            command = self.ui.get_command()
            if self.is_exit(command):
                break
            elif self.is_load(command):
                df = self.storage.load(sheet=command[1], index_col="Date")
                print(df)
            elif self.is_save(command):
                self.storage.save(df, sheet=command[1])
            elif self.is_download(command):
                series = self.downloader.download(org=command[1],
                                                  period=self._str_to_timedelta(command[2]),
                                                  interval=command[3])
                df = self._calculate_dataframe(series=series,
                                               interval=command[3],
                                               window=command[4])
            elif self.is_draw(command):
                self.ui.get_plot(df, command[1:])
            elif self.is_help(command):
                self.ui.get_help()


if __name__ == "__main__":
    pass
