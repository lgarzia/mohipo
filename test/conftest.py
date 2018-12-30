
import sys
import os
import pytest
import tempfile

from ..app import create_app, db

@pytest.fixture()
def add_mohipo_to_sys_path():
    split_name = __file__.split(os.sep)[:-3]  # get back to directory above mohipo to import package
    #os.sep.join(os.getcwd().split(os.sep)[:-1])
    package_path = os.sep.join(split_name)
    sys.path.append(package_path)

    yield

    sys.path.remove(package_path)


@pytest.fixture
def flask_app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def flask_client(flask_app):
    return flask_app.test_client()