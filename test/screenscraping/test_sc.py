import pytest
from selenium.webdriver import Chrome, Firefox
from os import sep
from collections import namedtuple
import requests
import datetime
import pytz
from bs4 import BeautifulSoup

Driver = namedtuple('Driver', ['name', 'exec_name', 'driver_class'], verbose=True)
drivers_to_try = [Driver('chrome', 'chromedriver.exe', Chrome), Driver('firefox', 'geckodriver.exe', Firefox)]

@pytest.fixture(params=drivers_to_try, ids= [n[0] for n in drivers_to_try])
def a_driver(request):
    return request.param #Boilerplate

def test_webdriver_module_drivers_location(add_mohipo_to_sys_path, a_driver):
    from mohipo.screenscraping import webdrivers as wd
    full_path = wd.WEBDRIVERS.get(a_driver.name, None)['exec_path']
    assert full_path.rsplit(sep, 4)[-4:] == ['mohipo', 'screenscraping', 'webdrivers', a_driver.exec_name]

#WEBDRIVERS['chrome'] = {'class_' : webdriver.Chrome, 'exec_path' : join(base_directory, 'chromedriver.exe')}
def test_webdriver_returns_class(add_mohipo_to_sys_path, a_driver):
    from mohipo import screenscraping as ss
    driver_detail = ss.get_driver_details(a_driver.name)
    assert driver_detail['class_'] == a_driver.driver_class

def test_webdriver_returns_exec_path(add_mohipo_to_sys_path, a_driver):
    from mohipo import screenscraping as ss
    driver_detail = ss.get_driver_details(a_driver.name)
    assert driver_detail['exec_path'].rsplit(sep, 4)[-4:] == ['mohipo', 'screenscraping', 'webdrivers', a_driver.exec_name]


@pytest.mark.skip(reason="long_test")
def test_webdriver_return_instance(add_mohipo_to_sys_path, a_driver):
    from mohipo import screenscraping as ss
    driver_instance = ss.get_browser(a_driver.name)
    print(type(driver_instance))
    test_cond = isinstance(driver_instance, a_driver.driver_class)
    if test_cond:
        driver_instance.close() #clean-up launches browser
    assert test_cond

#Test form entry/instructions
#


#************************************************************

@pytest.fixture()
def a_instr(add_mohipo_to_sys_path):
    from mohipo.screenscraping.mohipo_form_instruction import MohipoFormInstruction
    m = MohipoFormInstruction()
    return m

@pytest.mark.instr
def test_mohipo_form_instruction_max_days(a_instr):
    assert a_instr.max_days == 365

@pytest.fixture()
def a_scraper(add_mohipo_to_sys_path):
    from mohipo.screenscraping.mohipo_form_instruction import MohipoFormInstruction
    from mohipo.screenscraping.scraper import Scraper
    from mohipo import screenscraping as ss
    browser = ss.get_browser('chrome')
    url = 'https://www.mshp.dps.missouri.gov/HP68/SearchAction'
    frm_instr = MohipoFormInstruction()
    s = Scraper(url, frm_instr, browser)
    return s

@pytest.mark.scrapper
def test_scraper_single_forms_list(a_scraper):
    assert len(a_scraper._form_ids_base[0].values) == 365

@pytest.mark.scrapper
def test_scraper_single_entries(a_scraper):
    assert a_scraper._get_single_entries_for_form() == []

@pytest.mark.scrapper
def test_scraper_multiple_entries(a_scraper):
    assert len(a_scraper._get_multiple_entries_for_form()) == 1

@pytest.mark.scrapper
def test_scraper_expand_values(a_scraper):
    exp_value_class = a_scraper._get_multiple_entries_for_form()[0]
    expanded_list = a_scraper._expand_value_class(exp_value_class)
    #print(expanded_list[:2])
    assert len(expanded_list) == 365

@pytest.mark.scrapper
def test_scraper_merge_values(a_scraper):
    se = a_scraper._get_single_entries_for_form()
    exp_value_class = a_scraper._get_multiple_entries_for_form()[0]
    expanded_list = a_scraper._expand_value_class(exp_value_class)
    merge_list = a_scraper._merge_single_with_expanded_vc(se, expanded_list)
    #print(merge_list[:2])
    assert len(merge_list) == 365

@pytest.mark.scrapper
def test_scraper_build_exec_plan(a_scraper):
    out = a_scraper._build_exec_plan()
    print(out[:2])
    assert len(out) == 365

@pytest.mark.scrapper
def test_form_population(a_scraper):
    assert a_scraper._instructions.get_submit_id() == "//input[@type='submit']"

@pytest.mark.skip()
@pytest.mark.webscrapper
def test_mohipo_title(a_scraper):
    a_scraper._navigate_to_url()
    assert a_scraper.browser.title == 'Missouri State Highway Patrol - Crash Reports'


@pytest.mark.webscrapper
def test_form_population(a_scraper):
    try:
        a_scraper._populate_form()
        assert True == True
    except:
        assert False == True


@pytest.fixture()
def a_crash_report():
    from bs4 import BeautifulSoup
    fpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\example_crash_report.html"
    with open(fpath, 'r', encoding='utf-8') as f:
        html_ = f.read()
    soup =  BeautifulSoup(html_, features='lxml')
    return soup

@pytest.fixture()
def a_empty_crash_report():
    from bs4 import BeautifulSoup
    fpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\example_crash_report_no_results_found.html"
    with open(fpath, 'r', encoding='utf-8') as f:
        html_ = f.read()
    soup = BeautifulSoup(html_, features='lxml')
    return soup


@pytest.mark.parse
def test_valid_search_result(a_crash_report, add_mohipo_to_sys_path):
    # Base Crash Report Result should how 1 table
    table_ = a_crash_report.select('table') #alternative .select_one('table')
    from mohipo.screenscraping.extractions import _is_empty_result
    assert _is_empty_result(table_) is False


@pytest.mark.parse
def test_invalid_search_result(a_empty_crash_report, add_mohipo_to_sys_path):
    # Base Crash Report Result should how 1 table
    table_ = a_empty_crash_report.select('table')  # alternative .select_one('table')
    print(table_)
    from mohipo.screenscraping.extractions import _is_empty_result
    assert _is_empty_result(table_) is True

    # #Next function -> extract table
    # table_ = soup.select_one('table')
@pytest.mark.parse
def test_extract_mohipo_report_record(a_crash_report, add_mohipo_to_sys_path):
    from mohipo.screenscraping.extractions import extract_mohipo_report, ReportRecord
    table_ = a_crash_report.select('table')
    trs = table_[0].select('tr')[1:] #ignore header row
    tr_ = trs[0] #grab one row to test
    tds_ = tr_.select('td')
    row = extract_mohipo_report(data_row=tds_)
    d = datetime.datetime(2017, 12, 8, 23, 40)
    timezone = pytz.timezone('US/Central')
    d_aware = timezone.localize(d)

    expected_result = ReportRecord(rpt_id='170781483',
                                   rpt_url='https://www.mshp.dps.missouri.gov/HP68/AccidentDetailsAction?ACC_RPT_NUM=170781483',
                                   name='NELSON, PEYTON A',
                                   age=19,
                                   city='ST. LOUIS',
                                   state='MO',
                                   injury_status='NO INJURY ',
                                   timestamp=d_aware,
                                   crash_county='ST. LOUIS',
                                   crash_location='INTERSTATE 55 NORTHBOUND AT BAYLESS AVENUE',
                                   troop='C')
    assert row  == expected_result

@pytest.mark.parse
def test_extract_mohipo_all_report_record(a_crash_report, add_mohipo_to_sys_path):
    from mohipo.screenscraping.extractions import extract_mohipo_report, extract_all_rows
    table_ = a_crash_report.select('table')[0]
    results = extract_all_rows(table_, extract_mohipo_report)
    assert len(results) == 57

@pytest.fixture()
def a_crash_report_detail():
    #TODO - replace with relative link
    fpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\example_crash_report_details.html"
    with open(fpath, 'r', encoding='utf-8') as f:
        html_ = f.read()
    soup = BeautifulSoup(html_, features='lxml')
    return soup

@pytest.mark.parse
def test_extract_mohipo_detail_crash_info_record(a_crash_report_detail, add_mohipo_to_sys_path):
    from mohipo.screenscraping.extractions import extract_mohipo_crash_info, CrashInfoRecord
    tables_ = a_crash_report_detail.find_all('table')
    crash_info = tables_[0]
    trs = crash_info.select('tr')[1:]  # ignore header row
    tds_ = trs[0].select('td')
    r = extract_mohipo_crash_info(tds_)
    d = datetime.datetime(2018, 12, 8, 19, 41)
    timezone = pytz.timezone('US/Central')
    d_aware = timezone.localize(d)
    er = CrashInfoRecord(rpt_id=180734111,
                         investigated_by='TPR J B DOYLE #224',
                         gps_latitude=36.5515555,
                         gps_longitude=-89.809388,
                         timestamp=d_aware,
                         county='NEW MADRID',
                         location='MO 153 SOUTH OF US 62',
                         troop='E')
    assert er == r


@pytest.mark.parse
def test_extract_mohipo_detail_veh_info_record(a_crash_report_detail, add_mohipo_to_sys_path):
    from mohipo.screenscraping.extractions import extract_mohipo_vehicle_info, VehicleInfoRecord
    tables_ = a_crash_report_detail.find_all('table')
    _info = tables_[1]
    trs = _info.select('tr')[1:]  # ignore header row
    tds_ = trs[0].select('td')
    rpt_id = 10
    r = extract_mohipo_vehicle_info(tds_, rpt_id)
    er = VehicleInfoRecord(rpt_id=10,
                           veh_num=1,
                           veh_description='2004 FORD EXPLORER',
                           veh_damage='MODERATE',
                           veh_disposition='LEFT ROADSIDE FOR REMOVAL',
                           veh_driver_name='BANDA, MARIA',
                           veh_driver_gender='FEMALE',
                           veh_driver_age=47,
                           veh_safety_device='YES',
                           veh_driver_city='HOLCOMB',
                           veh_driver_state='MO',
                           veh_driver_insurance='DAIRYLAND AUTO',
                           veh_direction='SOUTHBOUND')
    assert er == r


@pytest.mark.parse
def test_extract_mohipo_detail_inj_info_record(a_crash_report_detail, add_mohipo_to_sys_path):
    from mohipo.screenscraping.extractions import extract_mohipo_injury_info, InjuryInfoRecord
    tables_ = a_crash_report_detail.find_all('table')
    _info = tables_[2]
    trs = _info.select('tr')[1:]  # ignore header row
    tds_ = trs[0].select('td')
    rpt_id = 10
    r = extract_mohipo_injury_info(tds_, rpt_id)
    er = InjuryInfoRecord(rpt_id=10,
                          veh_num=1,
                          name='BANDA, MARIA',
                          gender='FEMALE',
                          age=47,
                          injury_type='MODERATE',
                          safety_device='YES',
                          city='HOLCOMB',
                          state=' MO',
                          involvement='DRIVER',
                          disposition='TAKEN BY AMBULANCE TO SOUTHEAST HEALTH OF STODDARD \n      COUNTY')
    assert r == er

@pytest.mark.parse
def test_extract_mohipo_detail_misc_info_record(a_crash_report_detail, add_mohipo_to_sys_path):
    from mohipo.screenscraping.extractions import extract_mohipo_misc_info, MiscInfoRecord
    tables_ = a_crash_report_detail.find_all('table')
    _info = tables_[3]
    trs = _info.select('tr')  # only on row
    tds_ = trs[0].select('td')
    rpt_id = 10
    r = extract_mohipo_misc_info(tds_, rpt_id)
    print(r)
    assert isinstance(r, MiscInfoRecord) #Painful lining up multiline test

@pytest.fixture()
def a_crash_report_detail_empty():
    fpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\example_crash_report_details_no_results.html"
    with open(fpath, 'r', encoding='utf-8') as f:
        html_ = f.read()
    soup = BeautifulSoup(html_, features='lxml')
    return soup

@pytest.mark.parse
def test_extract_mohipo_detail_no_record(a_crash_report_detail_empty, add_mohipo_to_sys_path):
    from mohipo.screenscraping.extractions import _is_empty_result
    # test_url_no_data = 'https://www.mshp.dps.missouri.gov/HP68/AccidentDetailsAction?ACC_RPT_NUM=170781483'
    soup = a_crash_report_detail_empty
    tables_ = soup.find_all('table')
    assert _is_empty_result(tables_) is True

#TODO -> Integration test using Request
#Next steps -> Loop through all details reports
#Built multithread for Now - Asynchio Latter
@pytest.mark.data
def test_create_sqlalchemy_engine(add_mohipo_to_sys_path):
    from mohipo.config import DevConfig
    from mohipo.utils.db_util import _create_engine
    from sqlalchemy.engine import Engine
    engine = _create_engine(DevConfig)
    assert isinstance(engine, Engine)
