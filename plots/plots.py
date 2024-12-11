import matplotlib.pyplot as plt
from pandas import DataFrame

class Drawer:
    def plot(self,
             data: DataFrame):
        self._plot_main(data)
        self._plot_diff(data)
        self._plot_autocor(data)
        plt.show()


    def _plot_main(self,
                   data: DataFrame):
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data["Open"])
        plt.plot(data.index, data["Movavg"])


    def _plot_diff(self,
                   data: DataFrame):
        plt.subplot(2, 2, 3)
        plt.plot(data.index, data["Diff"])


    def _plot_autocor(self,
                      data: DataFrame):
        plt.subplot(2, 2, 4)
        plt.plot(data.index, data["Autocor"])
