from .form_instructions import ValueClass, FormInstructions
from .. utils.dates_util import get_last_range_date
# get_last_range_date(self, max_days: int, timezone_:str='US/Central', fmt: str="%m/%d/%Y")

class MohipoFormInstruction(FormInstructions):

    def __init__(self):
        super().__init__()
        self.max_days = 365

    def get_form_ids_values(self):
        """return iterable of ValueClass
        The data form just needs to complete date. It's a select without
        multiple selected
        """
        return [ValueClass(
                xpath="//*[@id='date']",
                values=get_last_range_date(self.max_days, 'US/Central', '%m/%d/%Y'),
                form_element_type='select',
                allow_multiple=False)]

    def get_submit_id(self):
        return super().get_submit_id()  # use default

