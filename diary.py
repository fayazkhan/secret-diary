#!/home/fayaz/Programming/weaver-env/bin/python
"""Fayaz's diary.

Usage:
  diary.py show <file>
  diary.py write <file> [--message=<message>] [--create]

Options:
  -h --help                       Show this screen.
  --version                       Show version.
  -m MESSAGE --message=MESSAGE    Message to add.
  --create                        Create tables if they don't exist.
"""
from getpass import getpass
import sys

import arrow
from sqlalchemy_utils import ArrowType
from docopt import docopt
from sqlalchemy import create_engine, Column, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def main():
    arguments = docopt(__doc__, version="Fayaz's diary 2.0")
    file = arguments['<file>']
    password = getpass(prompt='Database password: ')
    engine = create_engine(
        'sqlite+pysqlcipher://:{password}@/{database}'.format(
            database=file, password=password))
    session = sessionmaker(bind=engine)()
    if arguments['show']:
        show(session)
    elif arguments['write']:
        if arguments['--create']:
            Base.metadata.create_all(bind=engine)
        write(session, message=arguments['--message'])


def show(session):
    for entry in session.query(Entry):
        print(entry.updated.humanize(), entry.content)


def write(session, message=None):
    now = arrow.utcnow()
    entry = Entry(created=now, updated=now, content=message or '')
    session.add(entry)
    session.commit()
    if not entry.content:
        for line in sys.stdin:
            entry.content += line
            entry.updated = arrow.utcnow()
            session.commit()


Base = declarative_base()


class Entry(Base):

    __tablename__ = 'entry'
    created = Column(ArrowType, primary_key=True)
    updated = Column(ArrowType, nullable=False)
    content = Column(UnicodeText, nullable=False)


if __name__ == '__main__':
    main()