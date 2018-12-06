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
@pytest.mark.skip(reason="not built")
def test_mohipo_title(add_mohipo_to_sys_path):
    from mohipo import screenscraping as ss
    #TODO -> add test to evaluate title

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
    m = MohipoFormInstruction()
    s = Scraper(m)
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