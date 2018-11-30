#Inspired by flask - use python configuration
import os
basedir = os.path.abspath(os.path.dirname(__file__)) #return directory of mohipo

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or ''