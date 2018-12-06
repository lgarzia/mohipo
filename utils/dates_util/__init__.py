from datetime import datetime, timedelta
from pytz import timezone
from typing import Sequence, Union


def get_last_range_date(max_days: int, timezone_:str='US/Central', fmt: str="%m/%d/%Y")->Union[Sequence[str], Sequence[datetime]]:
    """If fmt None returns base DateTime"""
    tz_ = timezone_ or 'utc' #Can't be None
    cur_date = datetime.now(tz=timezone('US/Central'))  # assume time is central
    if fmt:
        return [(cur_date - timedelta(days=r)).strftime(fmt) for r in range(0, max_days)]
    else:
        return [(cur_date - timedelta(days=r)).strftime(fmt) for r in range(0, max_days)]