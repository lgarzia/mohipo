"""
Module defines Scraper Base Class
"""
from .form_instructions import FormInstructions, ValueClass
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.support.ui import Select
from toolz import curry
from typing import List, Union
from bs4 import BeautifulSoup

#class ValueClass(NamedTuple):
#    xpath: str
#    values: Union[str, Sequence[str]]
#    form_element_type: str
#    allow_multiple: bool

def _scrape_make_soup(html_:str, storage_path:str)->None:
    soup = BeautifulSoup(str)
    return soup


class Scraper:

    def __init__(self, url:str, instructions: FormInstructions, browser:Union[Chrome, Firefox]):
        self._instructions = instructions
        self._form_ids_base = instructions.get_form_ids_values()
        self._total_instr = []
        self.browser = browser
        self.url = url
        self.final_instruction_plan = self._build_exec_plan()

    def _get_single_entries_for_form(self)->List[ValueClass]:
        return [v for v in self._form_ids_base if v.values is str or v.allow_multiple is True]

    def _get_multiple_entries_for_form(self):
        return [v for v in self._form_ids_base if v.allow_multiple is False]

    def _expand_value_class(self, vc:ValueClass)->List[ValueClass]:
        @curry
        def make_value_class(xpath, form_element_type, allow_multiple, values):
            return ValueClass(xpath, values, form_element_type, allow_multiple)

        xpath, values, form_element_type, _ = vc
        make_value = make_value_class(xpath, form_element_type, False)
        return [make_value(v) for v in values]

    def _merge_single_with_expanded_vc(self, sl: List[ValueClass], xl: List[ValueClass])->List[List[ValueClass]]:
        def b(s1, vc):
            if sl:
                return sl.extend(vc)
            else:
                return [vc]
        return [b(sl,vc) for vc in xl]

    def _build_exec_plan(self):
        # Step 1 -> extract isolate single value from multiple values
        single_entries = self._get_single_entries_for_form()
        # Step 2 -> extract multiple entries
        multiple_entries = self._get_multiple_entries_for_form()
        #TODO -> scale up if multiple single dropdowns - not a problem for now to solve
        # Step 3 -> extract to list ValueClass
        exploded_entries = self._expand_value_class(multiple_entries[0]) #TODO-> clean_up
        #Step 4 put together everything
        final_out_put = self._merge_single_with_expanded_vc(single_entries, exploded_entries)
        return final_out_put

    def _navigate_to_url(self):
        self.browser.get(self.url)

    def _populate_form(self, vcl: List[ValueClass]):
        '''Refactor'''
#        self._navigate_to_url()
#        for vc in self.final_instruction_plan[-1]:
        for vc in vcl:
            if vc.form_element_type == 'select':
                if vc.allow_multiple:
                    #TODO -> build this
                    pass
                else:
                    element = Select(self.browser.find_element_by_xpath(vc.xpath))
                    element.select_by_value(vc.values)
            #Completed form entry -> Bare bones for scenario 1
#            print(self._instructions.get_submit_id())
#            submit = self.browser.find_element_by_xpath(self._instructions.get_submit_id())
#            submit.click()
            html_ = self.browser.page_source
            #scrape_table(html)

    def collect_base_htmls(self):
        import time
        self._navigate_to_url()
        print('navigated')
        all_html = []
        for vc in self.final_instruction_plan:
            print(vc, type(vc))
            print(self.browser.current_url)
            assert self.url == self.browser.current_url
            self._populate_form(vc)
            submit = self.browser.find_element_by_xpath(self._instructions.get_submit_id())
            submit.click()
            time.sleep(2)
            #TODO Terrible Code -> need more resiliency... wrap in retry decorator -> think hwo to write results one at time
            if self.url != self.browser.current_url:
                print('catching my breath')
                time.sleep(5)
                self.browser.back()
                time.sleep(2)
                self._populate_form(vc)
                submit = self.browser.find_element_by_xpath(self._instructions.get_submit_id())
                submit.click()
                time.sleep(2)
            html_ = self.browser.page_source
            all_html.append(html_) #TODO would like to capture dates
            print(self.url)
            time.sleep(5) #Site must be throttled -> Wait between each call
            self.browser.back()
        return all_html

    def __str__(self):
        return 'a_string' #TODO

