"""
Module defines Scraper Base Class
"""
from .form_instructions import FormInstructions, ValueClass
from itertools import combinations
from toolz import curry
from typing import List

#class ValueClass(NamedTuple):
#    xpath: str
#    values: Union[str, Sequence[str]]
#    form_element_type: str
#    allow_multiple: bool

class Scraper:

    def __init__(self, instructions: FormInstructions):
        self._instructions = instructions
        self._form_ids_base = instructions.get_form_ids_values()
        self._total_instr = []

    def _get_single_entries_for_form(self):
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

    def _build_combination(self, entries: List[List[ValueClass]])->List[ValueClass]:
        return combinations(*entries)

    def _build_exec_plan(self):
        # Step 1 -> extract isolate single value from multiple values
        single_entries = self._get_single_entries_for_form(self)
        # Step 2 -> extract multiple entries
        multiple_entries = self._get_multiple_entries_for_form()
        # Step 3 -> extract to list ValueClass
        #Return List of List
        exploded_entries = [self._expand_value_class(vc) for vc in multiple_entries]
        combined_entries = self._build_combination(*exploded_entries)
        #Step 4 put together everything
        final_out_put = [t.extend(single_entries) for t in combined_entries]

        return final_out_put



