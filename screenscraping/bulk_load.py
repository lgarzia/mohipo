'''

This module develop downloads initial data set from
Missouri Accident reports

Example:
    The initial download
        $ download(output, date_range)

Attributes:
'''
import os
import sys
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))

import pickle
from typing import Union
from selenium.webdriver import Chrome, Firefox
from mohipo.screenscraping import get_browser
from mohipo.config import DevConfig
from mohipo.utils.dates_util import get_last_range_date
BROWSER_VERSION = 'chrome'
from mohipo.screenscraping.mohipo_form_instruction import MohipoFormInstruction
from mohipo.screenscraping.scraper import Scraper

def get_url(webdriver_instance:Union[Chrome, Firefox], url_to_scrape:str)->Union[Chrome, Firefox]:
    webdriver_instance.get(url_to_scrape)


def _get_data_directory()->str:
    fpath = os.path.abspath(__file__)
    ddir = os.path.join(os.sep.join(fpath.split(os.sep)[:-2]), 'data')
    return ddir

HTMLS = None
#MAIN LOGIC
if __name__ == '__main__':
    w = get_browser(BROWSER_VERSION) #Wrap in context manager to close browser
    base_url = DevConfig.MOHIPO_SEARCH_PAGE
    print(base_url)
    f = MohipoFormInstruction()
    #Navigate to url
    s = Scraper(base_url, f, w)
    HTMLS = s.collect_base_htmls()
    w.close()
    ddir = _get_data_directory()
    print(ddir)
    ppath = os.path.join(ddir, 'htmls.pkl')
    with open(ppath, 'wb') as f:
        pickle.dump(HTMLS, f)



    with open(ppath, 'rb') as f:
        htmlsp = pickle.load(f)

    assert htmlsp == HTMLS