from sqlalchemy_utils import ArrowType, force_instant_defaults
from pysqlcipher3 import dbapi2 as sqlcipher
from sqlalchemy import create_engine, Column, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_database_session(file, password):
    engine = create_engine(
        'sqlite+pysqlcipher://:{password}@/{database}'.format(
            database=file, password=password), module=sqlcipher)
    session = sessionmaker(bind=engine)()
    return session


def create_entry(session, message=''):
    now = arrow.utcnow()
    entry = Entry(created=now, updated=now, content=message)
    session.add(entry)
    session.commit()
    return entry


force_instant_defaults()
Base = declarative_base()


class Entry(Base):

    __tablename__ = 'entry'
    created = Column(ArrowType, primary_key=True)
    updated = Column(ArrowType, nullable=False)
    content = Column(UnicodeText, nullable=False, default='')
