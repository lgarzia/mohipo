'''Create a base class of expected Selenium instructions'''

import abc

class FormInstructions(metaclass=abc.ABCMeta):
    '''
    TODO -> overall standard instruction for completing Form
    '''

    @abc.abstractmethod
    def get_form_ids_values(self):
        """return iterable of (xpath, values)"""

    @abc.abstractmethod
    def get_submit_id(self):
        """return submit button"""

    @abc.abstractmethod
    def process_form(self):
        """process form"""

class SeleniumFormInstruction(FormInstructions):
    '''Selenium Version of Form Instructions'''
    def __init__(self, _webdriver):
        self._webdriver = _webdriver

    def get_form_ids_values(self):
