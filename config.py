#Inspired by flask - use python configuration
import os
basedir = os.path.abspath(os.path.dirname(__file__)) #return directory of mohipo


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'data', 'mohipo_app.db')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MOHIPO_SEARCH_PAGE = os.environ.get('MOHIPO_SEARCH_PAGE') or 'https://www.mshp.dps.missouri.gov/HP68/SearchAction'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN = os.environ.get('ADMIN')

    def __repr__(self):
        return str([(k, v) for k, v in vars(Config).items() if not k.startswith('__')])

#   From Miguel's tutorial -> hook if want to add modifications
    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    pass

config = {
    'development': DevConfig,
    'default': DevConfig
}