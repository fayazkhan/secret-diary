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
from docopt import docopt

from diary import create_entry, create_database_session, Base


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


def write_from_buffer(session, buffer):
    entry = create_entry(session)
    for line in buffer:
        entry.content += line
        entry.updated = arrow.utcnow()
        session.commit()


def show(session):
    for entry in session.query(Entry):
        display_row(entry.updated.humanize(), entry.content)


def display_row(time, text):
    print(time, text)
