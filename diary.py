#!/home/fayaz/Programming/weaver-env/bin/python
"""Fayaz's diary.

Usage:
  diary show <file>
  diary write <file> [--message=<message>] [--create]

Options:
  -h --help                       Show this screen.
  --version                       Show version.
  -m MESSAGE --message=MESSAGE    Message to add.
  -c --create                        Create tables if they don't exist.
"""
from getpass import getpass
import sys

import arrow
from sqlalchemy_utils import ArrowType, force_instant_defaults
from docopt import docopt
from pysqlcipher3 import dbapi2 as sqlcipher
from sqlalchemy import create_engine, Column, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def main():
    arguments = docopt(__doc__, version="Fayaz's diary 2.0")
    file = arguments['<file>']
    password = getpass(prompt='Database password: ')
    session = create_database_session(file, password)
    if arguments['show']:
        show(session)
    elif arguments['write']:
        if arguments['--create']:
            Base.metadata.create_all(bind=session)
        if arguments['--message']:
            create_entry(session, message=arguments['--message'])
        else:
            write_from_buffer(session, sys.stdin)


def create_database_session(file, password):
    engine = create_engine(
        'sqlite+pysqlcipher://:{password}@/{database}'.format(
            database=file, password=password), module=sqlcipher)
    session = sessionmaker(bind=engine)()
    return session


def show(session):
    for entry in session.query(Entry):
        display_row(entry.updated.humanize(), entry.content)


def display_row(time, text):
    print(time, text)


def create_entry(session, message=''):
    now = arrow.utcnow()
    entry = Entry(created=now, updated=now, content=message)
    session.add(entry)
    session.commit()
    return entry


def write_from_buffer(session, buffer):
    entry = create_entry(session)
    for line in buffer:
        entry.content += line
        entry.updated = arrow.utcnow()
        session.commit()


force_instant_defaults()
Base = declarative_base()


class Entry(Base):

    __tablename__ = 'entry'
    created = Column(ArrowType, primary_key=True)
    updated = Column(ArrowType, nullable=False)
    content = Column(UnicodeText, nullable=False, default='')


if __name__ == '__main__':
    main()
