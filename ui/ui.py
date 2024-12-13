from pandas import DataFrame

from ui.plots import Drawer


class UserInterface:
    def __init__(self):
        self.__drawer = Drawer()

    def get_command(self) -> list[str]:
        '''
        Метод получения команды.

        Returns:
            Массив, состоящий из команды и аргументов.
        '''
        return self._command_to_list(input())

    def get_plot(self,
                 df: DataFrame,
                 columns: list[str]):
        self.__drawer.plot(df, columns)

    def get_help(self):
        print("Список команд:")
        print("exit - завершить программу.")
        print("load [sheet name] - загрузить страницу [sheet name] из .xslx файла.")
        print("save [sheet name] - сохранить данные в страницу [sheet name] .xslx файла.")
        print("download [organization] [period] [interval] [window] - загружает данные указанно компании за указанный интервал с определенным периодом." +
            "Вычисляет все данные с указанным окном скользящего среднего.")
        print("draw [list of cols] - Отобразить графики рассчитанных значений.")

    def _command_to_list(self,
                         command: str) -> list[str]:
        '''
        Метод переводящий строку в массив строк.

        Args:
            command: Строка которую нужно разделить.
        Returns:
            Массив строк.
        '''
        return command.split(" ")


if __name__ == "__main__":
    pass
