
from datetime import datetime
import time


def adapt_datetime(timestamp: datetime):
    return time.mktime(timestamp.timetuple())


def register():
    import sqlite3

    sqlite3.register_adapter(datetime, adapt_datetime)
