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

    def __str__(self):
        return 'a_string' #TODO

