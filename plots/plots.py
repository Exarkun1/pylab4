import matplotlib.pyplot as plt
from pandas import DataFrame
import math

from matplotlib.widgets import Button

class Drawer:
    '''
    Класс для отрисовки графиков
    '''

    def plot(self,
             data: DataFrame, columns: list) -> None:
        '''
        Отрисовывает несколько графиков, по одному на каждый временной ряд
        Входные параметры:
            data - Таблица с данными для отрисовки
            columns - Названия столбцов, графики которых надо отрисовать
        '''

        # Проверка на корректность введенных столбцов
        for column in columns:
            if not (column in list(data.columns.values)):
                print("Неверное название столбца: ", column)
                return

        self._data = data
        # Хранение всех рисунков на изображении для возможности редактирования
        self._axs = []
        self._fig = plt.figure()
        self._cols = columns
        
        self._nrows = math.ceil(len(columns) / 2)
        self._ncols = 2
        if len(columns) == 1:
            self._ncols = 1

        # Определение кнопки 
        resetax = self._fig.add_axes([0.8, 0.025, 0.1, 0.04])
        button = Button(resetax, 'Reset', hovercolor='0.975')
        button.on_clicked(self._reset);

        # Отрисовка всех графиков
        for i in range(0, len(columns)):
            if (i == (len(columns) - 1)) and len(columns) % 2 == 1:
                self._plot(columns[i], (i + 1, i + 2))
            else:
                 self._plot(columns[i], i + 1)

        plt.show()
    
    def _reset(self, event) -> None:
        '''
        Функция сборса масштаба всех графиков по обоим осям.
        Используется, так как неудобно сбрасывать масштаб встроенными средствами matplotlib
        '''
        
        for i in range(0, len(self._axs)):
            self._axs[i].set_xlim(self._data.index[0], self._data.index[-1])
            self._axs[i].set_ylim(self._data[self._cols[i]].min(), self._data[self._cols[i]].max())
        plt.show()         


    def _plot(self,
                column: str, coord: int) -> None:
        '''
            Функция отрисовки одного графика на изображении
            Входные параметры: 
                column - название столбца, по которому необходимо построить график
                coord - координаты графика на изображении
        '''
        
        ax = self._fig.add_subplot(self._nrows, self._ncols, coord)
        ax.plot(self._data.index, self._data[column])
        ax.set_title(column)
        self._axs.append(ax) 