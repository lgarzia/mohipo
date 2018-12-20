from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import NamedTuple, MutableMapping, List, Union, Optional
from sqlalchemy import Table, Column, DateTime, Integer, String, MetaData, Float, ForeignKey
from sqlalchemy.engine.result import ResultProxy
import inspect


import datetime
from types import MappingProxyType

#Typing Alias
stypes = Union[String, Integer, DateTime, Float]
ptypes = Union[str, int, datetime.datetime, float]
mmt = MutableMapping[ptypes, stypes]

def _build_pytpe_mapper()-> MappingProxyType:
    PYTHON_SQL_AL_DM: mmt = {str: String,
                             int: Integer,
                             datetime.datetime: DateTime,
                             float: Float
                             }
    return MappingProxyType(PYTHON_SQL_AL_DM)

PYTHON_SQL_AL_DM = _build_pytpe_mapper() #Exposing View of Mapping


def _create_engine(config: object)-> Engine:
    url_ = config.SQLALCHEMY_DATABASE_URI
    return create_engine(url_)

def _create_table_definition(Record:NamedTuple, metadata:MetaData)->Table:
    #TODO -> future enhancement worry about PK/FK
    table_name = Record.__name__
    col_list:List[Column] = []
    for col_name, col_type in Record.__annotations__.items():
        #check if tpying class/union
        satype:stypes = None
        print(col_type.__module__)
        if col_type.__module__ == 'typing':
            #check if Union -> know to loop
            if col_type.__class__ is type(Union):
                for t in col_type.__args__:
                    if t is type(None):
                        pass #skip
                    else:
                        satype = PYTHON_SQL_AL_DM[t]
                        break
        else:
            satype = PYTHON_SQL_AL_DM[col_type]
        col_list.append(Column(col_name, satype))
    return Table(table_name, metadata, *col_list)

def _generate_metadata(engine:Engine)->MetaData:
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata


def insert_record(table_name: str, record: NamedTuple,
                    metadata: MetaData, engine: Engine)->ResultProxy:
    table_ = metadata.tables[table_name]
    ins = table_.insert().values(record)
    conn = engine.connect() #TODO -> test success
    return conn.execute(ins)

#TODO -> build this out
#def truncate_table():
#    DELETE FROM  table_name;

#TODO move to test
#metadata = MetaData() #Call passes in Metadata
#table_ =  _create_table_definition(ReportRecord, metadata)


#Introspection Notes
#sig = inspect.signature(ReportRecord)
#ReportRecord.__annotations__
#ReportRecord._fields
#ReportRecord._field_types
#ReportRecord._field_defaults
#ReportRecord.__name__
#ReportRecord.__qualname__
#ReportRecord.__module__

