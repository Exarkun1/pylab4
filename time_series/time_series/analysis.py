import numpy as np
from pandas import DataFrame, Series, Index
from datetime import timedelta

class TimeSeriesAnalyser:
    def __init__(self,
                 series: Series,
                 interval: timedelta=None):
        self.__series = series
        self.__interval = None

        if interval is None:
            self.__interval = self.index[1] - self.index[0]
            for i in range(2, self.__series.size):
                interval = self.index[i] - self.index[i-1]
                if self.__interval > interval:
                    self.__interval = interval
        else:
            self.__interval = interval


    @property
    def size(self) -> int:
        return self.__series.size
    
    
    @property
    def index(self) -> Index:
        return self.__series.index
    
    
    @property
    def interval(self) -> timedelta:
        return self.__interval
    
    
    @property
    def series(self) -> Series:
        return self.__series
    
    
    def find_extremes(self,
                      glb: bool=False) -> DataFrame:
        if glb:
            return self._find_glb_extremes()
        else:
            return self._find_loc_extremes()


    def _find_glb_extremes(self) -> DataFrame:
        ids = [np.argmin(self.series), np.argmax(self.series)]
        return DataFrame({"Extreme": self.series.iloc[ids], "Type": ["Min", "Max"]},
                         index=self.index[ids])
    

    def _find_loc_extremes(self) -> DataFrame:
        ids = []
        types = []
        
        for i in range(1, -1):
            if self.series[i] <= self.series[i-1] and self.series[i] <= self.series[i+1]:
                ids.append(i)
                types.append("Min")
            elif self.series[i] >= self.series[i-1] and self.series[i] >= self.series[i+1]:
                ids.append(i)
                types.append("Max")

        return DataFrame({"Extreme": self.series.iloc[ids], "Type": types}, 
                         index=self.index[ids])
    
    
    def differentiate(self) -> Series:
        intervals = (self.index[1:] - self.index[:-1]) / self.interval
        diffs = (self.series.values[1:] - self.series.values[:-1])

        return Series(diffs / intervals, index=self.index[:-1], name="Diff")
    

    def calc_movavg(self,
                    window: int|timedelta) -> Series:
        movavgs = None
        if isinstance(window, int):
            movavgs = self._calc_movavg_int(window)
        if isinstance(window, timedelta):
            movavgs = self._calc_movavg_timedelta(window)
        return movavgs
    
    
    def _calc_movavg_int(self,
                         window: int) -> Series:
        if window < 1:
            error = ValueError("Попытка передачи отрицательного окна.")
            raise error
        
        movavgs = np.empty(self.size, dtype=float)
        for i in range(0, self.size):
            start_pos = i - window + 1
            if start_pos < 0:
                start_pos = 0
            movavgs[i] = np.average(self.series.values[start_pos:i+1])

        return Series(movavgs, index=self.index, name="Movavg")
    
    
    def _calc_movavg_timedelta(self,
                               window: timedelta):
        movavgs = np.empty([self.size], dtype=float)
        for i in range(0, self.size):
            sum_prices = 0
            n = 0
            for j in range(i, -1, -1):
                interval = self.index[i] - self.index[j]
                if interval <= window:
                    sum_prices += self.series.values[j]
                    n += 1
                else:
                    break
            movavgs[i] = sum_prices / n

        return Series(movavgs, index=self.index, name="Movavg")
    
    
    def calc_autocor(self) -> Series:
        autocors = np.empty([self.size-1])
        for i in range(0, self.size-1):
            x = self.series.values[i:]
            y = self.series.values[:self.size-i]
            avg_x = np.average(x)
            avg_y = np.average(y)
            avg_xy = np.average(x*y)
            std_x = np.std(x)
            std_y = np.std(y)
            autocors[i] = (avg_xy - avg_x*avg_y) / (std_x*std_y)

        return Series(autocors, index=self.index[:-1], name="Autocor")
    

if __name__ == "__main__":
    pass