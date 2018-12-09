import pytest
from selenium.webdriver import Chrome, Firefox
from os import sep
from collections import namedtuple


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


@pytest.mark.parse
def test_make_soup():
    from bs4 import BeautifulSoup
    from bs4 import El
    fpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\example_crash_report.html"
    with open(fpath, 'r', encoding='utf-8') as f:
        html_ = f.read()

    soup =  BeautifulSoup(html_, features='lxml')
    assert isinstance(soup, BeautifulSoup)

    #Next function -> extract table
    table_ = soup.select_one('table')
    table_.select('tr')
    tpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\table_example.html"

    from typing import NamedTuple, Union
    import datetime
    class ReportRecord(NamedTuple):
        rpt_id: int
        rpt_url: str
        name: [None, str]
        age: Union[None, int]
        city: [None, str]
        state: [None, str]
        injury_status: [None, str]
        timestamp: [None, datetime.datetime]
        crash_county: [None, str]
        crash_location: [None, str]
        troop:[None, str]



    with open(tpath, 'w', encoding='utf-8') as f:
        f.write(str(table_.prettify(encoding='utf-8')))
        table_.get()
        th = table_.select('th')
        headers_ = [t.text.strip() for t in th]
        trs = table_.select('tr')[1:] #ignore header row
        tr_ = trs[0]
        tds_ = tr_.select('td')
        #isolate link to view report
        #need a_href & isolate ACC_RPT_NUM -> key to join on
        rpt_url = tds_[0].find('a').get('href')
        regex = '.*ACC_RPT_NUM=(?P<rpt_name>.*)$'
        import re
        m = re.match(regex, rpt_url)
        rpt_id = m.group('rpt_name')
        name = tds_[1].text
#        age: int
        age = int(tds_[2].text) if  tds_[2].text != '' else None
        city_state = tds_[3].text if tds_[3].text != '' else None
        if city_state:
            city, state = [t.strip() for t in city_state.split(",")]
        else:
            city, state = [None,None]
        injury_status = tds_[4].text if tds_[4] !='' else None
#        injury_status: str
                        tds_[5].text #date
                        tds_[6].text #time
                        pdte = '%m/%d/%Y'
                        pdte_time = '%m/%d/%Y_%I:%M%p'
                        import datetime
                        from pytz import timezone
                        tz_u = datetime.datetime.strptime(tds_[5].text+'_'+tds_[6].text,pdte_time)
                        from pytz import timezone
                        timestamp = timezone('US/Central').localize(tz_u)
                        #TODO -> wrap condition checks for missing date/times scenarios

                        crash_county = tds_[7].text
                        crash_location = tds_[7].text
                        troop = tds_[7].text