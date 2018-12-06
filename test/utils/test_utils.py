import pytest
from os import sep
from collections import namedtuple

@pytest.mark.dates
def test_get_last_range_date(add_mohipo_to_sys_path):
    from mohipo.utils.dates_util import get_last_range_date
    r = get_last_range_date(5)
    assert len(r) == 5