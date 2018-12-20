
import sys
import os
import pytest

@pytest.fixture()
def add_mohipo_to_sys_path():
    split_name = __file__.split(os.sep)[:-3]  # get back to directory above mohipo to import package
    #os.sep.join(os.getcwd().split(os.sep)[:-1])
    package_path = os.sep.join(split_name)
    sys.path.append(package_path)

    yield

    sys.path.remove(package_path)


