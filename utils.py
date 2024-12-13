from pandas import Series, DataFrame
from datetime import timedelta
from time_series import TimeSeriesAnalyser

def str_to_timedelta(period: str) -> timedelta:
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

def command_to_list(comand: str) -> list[str]:
    return comand.split(" ")

def calculate_dataframe(series: Series,
                        interval: str,
                        window: str) -> DataFrame:
    analyser = TimeSeriesAnalyser(series, str_to_timedelta(interval))
    movavg = analyser.calc_movavg(str_to_timedelta(window))
    analyser = TimeSeriesAnalyser(movavg, str_to_timedelta(interval))
    diff = analyser.differentiate()
    autocor = analyser.calc_autocor()
    return DataFrame({"Open": series, "Movavg": movavg, "Diff": diff, "Autocor": autocor})