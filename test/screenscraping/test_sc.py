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
    fpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\example_crash_report.html"
    with open(fpath, 'r', encoding='utf-8') as f:
        html_ = f.read()

    soup =  BeautifulSoup(html_, features='lxml')
    assert isinstance(soup, BeautifulSoup)

    #TODO -> check if results found
    fpath = r"C:\Users\lgarzia\Documents\apps\mohipo\test\screenscraping\example_crash_report_no_results_found.html"
    with open(fpath, 'r', encoding='utf-8') as f:
        html_ = f.read()

    soup =  BeautifulSoup(html_, features='lxml')
    table_ = soup.select_one('table')
    if table_:
        pass#Scrape
    else:
        print('No Data - skipping')
    len(table_)


    #Next function -> extract table
    table_ = soup.select_one('table')
    #TODO -> check if "no data"
    table_.select('tr')
    th = table_.select('th')
    headers_ = [t.text.strip() for t in th]
    trs = table_.select('tr')[1:] #ignore header row
    #Loop through each row
    tr_ = trs[0]
    tds_ = tr_.select('td')#Pass through function -> create
    import sys
    sys.path.append(r"C:\Users\lgarzia\Documents\apps")
    from mohipo.screenscraping.extractions import extract_mohipo_report
    row =  extract_mohipo_report(data_row = tds_)
    base_report = []
    for r in trs:
        rc = extract_mohipo_report(data_row = tds_)
        base_report.append(rc)
    len(base_report)

    #next step is linking to anchor
    test_url = 'https://www.mshp.dps.missouri.gov/HP68/AccidentDetailsAction?ACC_RPT_NUM=180734111'
    import requests
    from bs4 import BeautifulSoup
    req = requests.get(test_url)
    soup_2 = BeautifulSoup(req.text,features='lxml')
    tables_ = soup_2.find_all('table')
    len(tables_) #TODO -> test condition here for empty pages(how to track?)
    #Table 1
    crash_info = tables_[0]
    #TODO -> abstract out looping through table
    trs = crash_info.select('tr')[1:]  # ignore header row
    len(trs)
    tds_ = trs[0].select('td')
    import sys
    sys.path.append(r"C:\Users\lgarzia\Documents\apps")
    from mohipo.screenscraping.extractions import extract_mohipo_crash_info, \
        extract_mohipo_vehicle_info, extract_mohipo_injury_info, \
        extract_mohipo_misc_info

    r = extract_mohipo_crash_info(tds_)
    #table 2
    #key is report id and veh_#
    rpt_id = r.rpt_id
    veh_info = tables_[1]
    trs = veh_info.select('tr')[1:]  # ignore header row
    len(trs)
    tds_ = trs[0].select('td')
    vr  = extract_mohipo_vehicle_info(tds_, rpt_id)

    #table 3
    inj_info = tables_[2]
    trs = inj_info.select('tr')[1:]  # ignore header row
    len(trs)
    tds_ = trs[0].select('td')
    vr = extract_mohipo_injury_info(tds_, rpt_id)

    #table 4
    misc_info = tables_[3]
    trs = misc_info.select('tr')  # only one row final table
    len(trs)
    tds_ = trs[0].select('td')
    mir = extract_mohipo_misc_info(tds_, rpt_id)

    #Check in table in empty
    test_url_no_data = 'https://www.mshp.dps.missouri.gov/HP68/AccidentDetailsAction?ACC_RPT_NUM=170781483'
    req = requests.get(test_url_no_data)
    soup_2 = BeautifulSoup(req.text,features='lxml')
    tables_ = soup_2.find_all('table')
    len(tables_) #TODO -> test condition here for empty pages(how to track?)
    if len(tables_) <= 1:
        trs = tables_[0].select('tr')  # only one row final table
        tds_ = trs[0].select('td')
        if tds_[0].text.strip() == 'NO CRASH DETAILS':
            print('No details')
        else:
            pass
            #TODO -> send for processing?
        #test if no crash report

