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


def test_webdriver_return_instance(add_mohipo_to_sys_path, a_driver):
    from mohipo import screenscraping as ss
    driver_instance = ss.get_browser(a_driver.name)
    print(type(driver_instance))
    test_cond = isinstance(driver_instance, a_driver.driver_class)
    if test_cond:
        driver_instance.close() #clean-up launches browser
    assert test_cond