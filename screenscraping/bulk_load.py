'''

This module develop downloads initial data set from
Missouri Accident reports

Example:
    The initial download
        $ download(output, date_range)

Attributes:
'''

from typing import Union
from selenium.webdriver import Chrome, Firefox
from . import get_browser()
BROWSER_VERSION = 'chrome'
def get_url(webdriver_instance:Union[Chrome, Firefox], url_to_scrape:str)->Union[Chrome, Firefox]:
    webdriver_instance.get(url_to_scrape)

#MAIN LOGIC
w = get_browser(BROWSER_VERSION)
