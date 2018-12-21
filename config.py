#Inspired by flask - use python configuration
import os
basedir = os.path.abspath(os.path.dirname(__file__)) #return directory of mohipo


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'data', 'mohipo.db')
    MOHIPO_SEARCH_PAGE = os.environ.get('MOHIPO_SEARCH_PAGE') or 'https://www.mshp.dps.missouri.gov/HP68/SearchAction'

    def __repr__(self):
        return str([(k, v) for k, v in vars(Config).items() if not k.startswith('__')])


class DevConfig(Config):
    pass
