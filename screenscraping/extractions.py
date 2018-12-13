"""Module defines functions that'll take a row of data
and return tuple records"""
import re
from typing import List, NamedTuple, Union, Callable
from numbers import Number
import datetime

from bs4 import Tag
from pytz import timezone


class ReportRecord(NamedTuple):
    rpt_id: int
    rpt_url: str
    name: Union[None, str]
    age: Union[None, int]
    city: Union[None, str]
    state: Union[None, str]
    injury_status: Union[None, str]
    timestamp: Union[None, datetime.datetime]
    crash_county: Union[None, str]
    crash_location: Union[None, str]
    troop: Union[None, str]


class CrashInfoRecord(NamedTuple):
    rpt_id: int
    investigated_by: Union[None, str]
    gps_latitude: Union[None, float]
    gps_longitude: Union[None, float]
    timestamp: Union[None, datetime.datetime]
    county: Union[None, str]
    location: Union[None, str]
    troop: Union[None, str]


#TODO -> split into more specific functions
def _process_date_fields(date_tag:Tag, time_tag:Tag,tz:str='US/Central',
                         date_fmt:str='%m/%d/%Y', datetime_fmt:str='%m/%d/%Y_%I:%M%p'
                         )->Union[None, datetime.datetime]:
    if date_tag !='':
        pdte = date_fmt
        pdte_time = datetime_fmt
        date_ = date_tag.text
        time_ = time_tag.text
        if time_ != '' and date_ != '':
            tz_u = datetime.datetime.strptime(date_ + '_' + time_, pdte_time)
        elif date_ != '':
            tz_u = datetime.datetime.strptime(date_, pdte)
        else:
            tz_u = None
        timestamp = timezone(tz).localize(tz_u) if tz_u else None
        return timestamp
    else:
        return None

def _process_text_or_none(t:Tag, conv: Callable=None)->Union[None, str, Number]:
    field = t.text if t.text != '' else None
    return conv(field) if conv else field

def extract_mohipo_report(data_row: List[Tag])->ReportRecord:
    """Given list of TD Tags"""
    # isolate link to view report
    # need a_href & isolate ACC_RPT_NUM -> key to join on
    rpt_url = data_row[0].find('a').get('href')
    regex = '.*ACC_RPT_NUM=(?P<rpt_num>.*)$'
    m = re.match(regex, rpt_url)
    rpt_id = m.group('rpt_num')
    name = data_row[1].text
    age = int(data_row[2].text) if data_row[2].text != '' else None
    city_state = data_row[3].text if data_row[3].text != '' else None
    if city_state:
        city, state = [t.strip() for t in city_state.split(",")]
    else:
        city, state = [None, None]
    injury_status = data_row[4].text if data_row[4] != '' else None
    pdte = '%m/%d/%Y'
    pdte_time = '%m/%d/%Y_%I:%M%p'
    date_ = data_row[5].text
    time_ = data_row[6].text
    if time_ != '' and date_ != '':
        tz_u = datetime.datetime.strptime(date_ + '_' + time_, pdte_time)
    elif date_ != '':
        tz_u = datetime.datetime.strptime(date_ , pdte)
    else:
        tz_u = None

    timestamp = timezone('US/Central').localize(tz_u) if tz_u else None

    crash_county = data_row[7].text if data_row[7].text != '' else None
    crash_location = data_row[8].text if data_row[8].text != '' else None
    troop = data_row[8].text if data_row[8].text != '' else None

    return ReportRecord(rpt_id, rpt_url, name, age, city, state,
                        injury_status, timestamp, crash_county,
                        crash_location, troop)


def extract_mohipo_crash_info(data_row: List[Tag])->CrashInfoRecord:
    investigated_by = _process_text_or_none(data_row[0])
    rpt_id = data_row[1].text  # Key
    gps_latitude = _process_text_or_none(data_row[2], float)
    gps_longitude = _process_text_or_none(data_row[3], float)  # TODO-> function extract text or None
    timestamp = _process_date_fields(data_row[4], data_row[5])
    county = _process_text_or_none(data_row[6])
    location = _process_text_or_none(data_row[7])
    troop = _process_text_or_none(data_row[8])
    return CrashInfoRecord(rpt_id=rpt_id,
                           investigated_by=investigated_by,
                           gps_latitude=gps_latitude,
                           gps_longitude=gps_longitude,
                           timestamp=timestamp,
                           county=county,
                           location=location,
                           troop=troop
                           )

