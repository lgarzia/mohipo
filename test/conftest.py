import pytest
#TODO -> move this to test_fixtures

import sys
import os
#base_package = r"C:\Users\lgarzia\Documents\apps\mohipo\test\conftest.py"

@pytest.fixture()
def add_mohipo_to_sys_path():
    split_name = __file__.split(os.sep)[:-3]  # get back to directory above mohipo to import package
    package_path = os.sep.join(split_name)
    sys.path.append(package_path)

    yield

    sys.path.remove(package_path)

