"""
Модуль тестирования работы класса обработки временных рядов.
"""
import unittest
import numpy as np
from pandas import Series
from datetime import timedelta, datetime
from time_series import TimeSeriesAnalyser

class TestStockAnalyser(unittest.TestCase):
    def setUp(self):
        data = Series(
            data=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            index=[
                datetime(2024, 9, 1),
                datetime(2024, 9, 2),
                datetime(2024, 9, 3),
                datetime(2024, 9, 4),
                datetime(2024, 9, 5),
                datetime(2024, 9, 6),
                datetime(2024, 9, 7),
                datetime(2024, 9, 8),
                datetime(2024, 9, 9),
            ]
            )
        self.stock_analyser = TimeSeriesAnalyser(data)

    def test_find_blobal_extremes(self):
        dataframe = self.stock_analyser.find_extremes(glb=True)
        self.assertEqual(dataframe["Extreme"].iloc[0], 1)
        self.assertEqual(dataframe["Extreme"].iloc[1], 9)

    def test_find_local_extremes(self):
        dataframe = self.stock_analyser.find_extremes()
        self.assertEqual(len(dataframe), 0)

    def test_differentiate(self):
        series = self.stock_analyser.differentiate()
        self.assertEqual(np.sum(series), 8)

    def test_calc_movavg_int(self):
        series = self.stock_analyser.calc_movavg(window=4)
        self.assertEqual(series.iloc[4], 3.5)

    def test_calc_movarg_timedelta(self):
        data = self.stock_analyser.calc_movavg(window=timedelta(days=3))
        self.assertEqual(data.iloc[4], 3.5)

    def test_calc_autocor(self):
        series = self.stock_analyser.calc_autocor()
        self.assertTrue(1 - series.iloc[4] < 1e12)

if __name__ == "__main__":
    unittest.main()

