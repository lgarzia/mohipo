'''Create a base class of expected Form Instructions
Idea ->
'''


import abc
from typing import List, NamedTuple, Union, Sequence
#TODO -> define a return class


class ValueClass(NamedTuple):
    xpath: str
    values: Union[str, Sequence[str]]
    form_element_type: str
    allow_multiple: bool


class FormInstructions(metaclass=abc.ABCMeta):
    '''
    TODO -> overall standard instruction for completing Form
    '''

    @abc.abstractmethod
    def get_form_ids_values(self)->Sequence[ValueClass]:
        """return iterable of (xpath, values)"""

    @abc.abstractmethod
    def get_submit_id(self):
        """return xpath for submit button"""
        return "//input[@type='submit']"