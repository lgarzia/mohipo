from .form_instructions import ValueClass, FormInstructions
from datetime import datetime, timedelta
from pytz import timezone


class MohipoFormInstruction(FormInstructions):

    def __init__(self):
        super().__init__()
        self.max_days = 365

    @staticmethod
    def _gen_date_values(self, max_days: int):
        cur_date = datetime.now(tz=timezone('US/Central'))  # assume time is central
        fmt = "%m/%d/%Y"
        return [(cur_date - timedelta(days=r)).strftime(fmt) for r in range(0, max_days)]

    def get_form_ids_values(self):
        """return iterable of ValueClass
        The data form just needs to complete date. It's a select without
        multiple selected
        """
        return [ValueClass(
                xpath="//*[@id='date']",
                values=self._gen_date_values(self.max_days),
                form_element_type='select',
                allow_multiple=False)]

    def get_submit_id(self):
        super().get_submit_id()  # use default

