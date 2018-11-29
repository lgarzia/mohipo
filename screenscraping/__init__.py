from .webdrivers import WEBDRIVERS
from typing import Union
from selenium.webdriver import Chrome, Firefox

def get_driver_details(name:str):
    return WEBDRIVERS[name]

def get_browser(name:str)->Union[Chrome, Firefox]:
    """
    return an instances of requested selenium driver

    driver should be downloaded - see PyPi selenium docs for details'

    Args:
        name: Name of browser (chrome, firefox)
    Returns:
        One of selenium.webdriver.Chrome, FireFox
    Raises:

    """
    browser_details = get_driver_details(name)
    return browser_details['class_'](executable_path=browser_details['exec_path'])

