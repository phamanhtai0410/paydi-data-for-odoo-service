# -*- coding: utf-8 -*-



# File: datetime.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from datetime import datetime, timedelta, date
from paydi_lib.exceptions import handle_exception

def get_current_time():
    return datetime.utcnow()


def get_expired_time(start: datetime, time: float):
    return datetime.fromtimestamp(
        start.timestamp() + time
    )

@handle_exception(default=datetime.utcnow, tracking=False)
def convert_datetime_from_string(date_str: str,
                                 format: str = "%Y%m%d%H%M%S") -> datetime:
    return datetime.strptime(date_str, format)


@handle_exception(default=datetime.utcnow, tracking=False)
def convert_date_from_string(date_str: str,
                             format: str = "%Y%m%d") -> date:
    return datetime.strptime(date_str, format).date()


def date_range(start: date, end: date):
    return [start + timedelta(n) for n in range(int((end - start).days) + 1)]


def days_between(d1: datetime, d2: datetime):
    return abs((d2 - d1).days)