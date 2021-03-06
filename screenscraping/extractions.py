"""Module defines functions that'll take a row of data
and return tuple records"""
import re
from typing import List, NamedTuple, Union, Callable, Optional
from numbers import Number
import datetime

from bs4 import Tag
from pytz import timezone

#TODO -> convert time to UTC before writing to DB
class ReportRecord(NamedTuple):
    rpt_id: int
    rpt_url: str
    name: Optional[str]
    age: Optional[int]
    city: Optional[str]
    state: Optional[str]
    injury_status: Optional[str]
    timestamp: Optional[datetime.datetime]
    crash_county: Optional[str]
    crash_location: Optional[str]
    troop: Optional[str]


class CrashInfoRecord(NamedTuple):
    rpt_id: int
    investigated_by: Optional[str]
    gps_latitude: Optional[float]
    gps_longitude: Optional[float]
    timestamp: Optional[datetime.datetime]
    county: Optional[str]
    location: Optional[str]
    troop: Optional[str]


class VehicleInfoRecord(NamedTuple):
    rpt_id: int
    veh_num: int
    veh_description: Optional[str]
    veh_damage: Optional[str]
    veh_disposition: Optional[str]
    veh_driver_name: Optional[str]
    veh_driver_gender: Optional[str]
    veh_driver_age: Optional[int]
    veh_safety_device: Optional[str]
    veh_driver_city: Optional[str]
    veh_driver_state: Optional[str]
    veh_driver_insurance: Optional[str]
    veh_direction: Optional[str]


class InjuryInfoRecord(NamedTuple):
    rpt_id: int
    veh_num: int
    name: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    injury_type: Optional[str]
    safety_device: Optional[str]
    city: Optional[str]
    state: Optional[str]
    involvement: Optional[str]
    disposition: Optional[str]


class MiscInfoRecord(NamedTuple):
    rpt_id: int
    misc_information: str


def _is_empty_result(tables_:List[Tag])->bool:
    num_tables = len(tables_)
    print(f"number of table {num_tables}")
    if num_tables == 0:
        return True #Empty Search Results -> No Tables
    if num_tables > 1:
        return False
    trs = tables_[0].select('tr') #first row header if valid
    tds_ = trs[0].select('td')
    if tds_:
        if tds_[0].text.strip() == 'NO CRASH DETAILS':
            return True
        else:
            return False
    return False #Default


def get_splitter(value: str)->str:
    if ',' in value:
        return ','
    elif '/' in value:
        return '/'
    else:
        print(f"Unknown Splitter {value}")
        return '****'

#TODO -> split into more specific functions
def _process_date_fields(date_tag:Tag, time_tag:Tag,tz:str='US/Central',
                         date_fmt:str='%m/%d/%Y', datetime_fmt:str='%m/%d/%Y_%I:%M%p'
                         )->Union[None, datetime.datetime]:
    if date_tag != '':
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
    field = t.text.strip() if t.text != '' else None
    try:
        return conv(field) if conv else field
    except ValueError:
        return None #Indicate invalid data
    return

#TODO -> refactor using helper functions
def extract_mohipo_report(data_row: List[Tag])->ReportRecord:
    """Given list of TD Tags"""
    # isolate link to view report
    # need a_href & isolate ACC_RPT_NUM -> key to join on
    rpt_url = data_row[0].find('a').get('href')
    regex = '.*ACC_RPT_NUM=(?P<rpt_num>.*)$'
    m = re.match(regex, rpt_url)
    rpt_id = m.group('rpt_num')
    name = _process_text_or_none(data_row[1])
    age = _process_text_or_none(data_row[2], int)
    city_state = _process_text_or_none(data_row[3])
    if city_state:
        print(city_state)
        if city_state.rfind(',') >= 0: #Records with No States
            city, state, *_ = [t.strip() for t in city_state.split(",")] #TODO regression test bad data -> HARDY, ARKANSAS  HARDY, ARKANSAS
        else:
            city, state = (city_state, None)
    else:
        city, state = [None, None]
    injury_status = _process_text_or_none(data_row[4])
    timestamp = _process_date_fields(data_row[5], data_row[6])

    crash_county = _process_text_or_none(data_row[7])
    crash_location = _process_text_or_none(data_row[8])
    troop = _process_text_or_none(data_row[9])
    return ReportRecord(rpt_id, rpt_url, name, age, city, state,
                        injury_status, timestamp, crash_county,
                        crash_location, troop)


def extract_mohipo_crash_info(data_row: List[Tag])->CrashInfoRecord:
    investigated_by = _process_text_or_none(data_row[0])
    rpt_id = int(data_row[1].text)  # Key
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

#TODO -> leverage a data validator library (changing schemas) -> simple (check len)
def extract_mohipo_vehicle_info(data_row: List[Tag], rpt_id:int)->VehicleInfoRecord:
    veh_num = int(data_row[0].text)
    veh_description = _process_text_or_none(data_row[1])
    veh_damage = _process_text_or_none(data_row[2])
    veh_disposition = _process_text_or_none(data_row[3])
    veh_driver_name = _process_text_or_none(data_row[4])
    veh_driver_gender = _process_text_or_none(data_row[5])
    veh_driver_age =  _process_text_or_none(data_row[6], int)
    veh_safety_device = _process_text_or_none(data_row[7])
    veh_location = _process_text_or_none(data_row[8])
    if veh_location:
        res_ = veh_location.split(get_splitter(veh_location))
        if len(res_) > 1:
            veh_driver_city, veh_driver_state, *_ = [r.strip() for r in res_]
        else:
            veh_driver_city = res_[0].strip()
            veh_driver_state = None
    else:
        veh_driver_city, veh_driver_state = None, None
    veh_driver_insurance = _process_text_or_none(data_row[9])
    veh_direction = _process_text_or_none(data_row[10])

    return VehicleInfoRecord(
        rpt_id=rpt_id,
        veh_num=veh_num,
        veh_description=veh_description,
        veh_damage=veh_damage,
        veh_disposition=veh_disposition,
        veh_driver_name=veh_driver_name,
        veh_driver_gender=veh_driver_gender,
        veh_driver_age=veh_driver_age,
        veh_safety_device=veh_safety_device,
        veh_driver_city=veh_driver_city,
        veh_driver_state=veh_driver_state,
        veh_driver_insurance=veh_driver_insurance,
        veh_direction=veh_direction)


def extract_mohipo_injury_info(data_row: List[Tag], rpt_id: int) -> InjuryInfoRecord:
    veh_num = int(data_row[0].text)
    name = _process_text_or_none(data_row[1])
    gender = _process_text_or_none(data_row[2])
    age = _process_text_or_none(data_row[3], int)
    injury_type = _process_text_or_none(data_row[4])
    safety_device = _process_text_or_none(data_row[5])
    location = _process_text_or_none(data_row[6])
    if location:
        res_ = location.split(get_splitter(location))
        if len(res_) > 1:
            city, state, *_ = [r.strip() for r in res_]
        else:
            city = res_[0].strip()
            state = None
    else:
        city, state = None, None
    involvement = _process_text_or_none(data_row[7])
    disposition = _process_text_or_none(data_row[8])

    return InjuryInfoRecord(
        rpt_id=rpt_id,
        veh_num=veh_num,
        name=name,
        gender=gender,
        age=age,
        injury_type=injury_type,
        safety_device=safety_device,
        city=city,
        state=state,
        involvement=involvement,
        disposition=disposition
        )


def extract_mohipo_misc_info(data_row: List[Tag], rpt_id: int) -> InjuryInfoRecord:
    misc_information = data_row[0].text
    return MiscInfoRecord(
                rpt_id=rpt_id,
                misc_information=misc_information)


def extract_all_rows(table: Tag, extractor: Callable, has_header=True)->List[NamedTuple]:
    dataset = []
    st_row = 1 if has_header else 0
    trs = table.select('tr')[st_row:]
    for r in trs:
        tds_ = r.select('td')
        rc = extractor(data_row = tds_)
        dataset.append(rc)
    return dataset

