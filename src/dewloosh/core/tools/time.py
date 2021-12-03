import datetime
from datetime import datetime as dt
from dateutil.parser import parse
from collections import Iterable


class Time(object):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.time = datetime.datetime.now()

    @staticmethod
    def now() -> dt:
        return datetime.datetime.now()

    @staticmethod
    def now_to_str() -> str:
        return str(Time.now())

    @staticmethod
    def date_to_str(date: dt) -> str:
        return str(date)

    @staticmethod
    def str_to_date(date: str) -> dt:
        return parse(date)

    @staticmethod
    def oldest(dates: Iterable, num=1) -> dt:
        if num > 1:
            ascending = Time.ascending(dates)
            if num > len(ascending):
                return ascending
            return ascending[0:num]
        else:
            return min(dates)

    @staticmethod
    def latest(dates: Iterable, num=1) -> dt:
        if num > 1:
            descending = Time.descending(dates)
            if num > len(descending):
                return descending
            return descending[0:num]
        else:
            return max(dates)

    @staticmethod
    def ascending(dates: Iterable) -> Iterable:
        return sorted(dates)

    @staticmethod
    def descending(dates: Iterable) -> Iterable:
        return sorted(dates, reverse=True)
