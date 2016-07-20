#    secret-diary: A secure diary app
#    Copyright (C) 2016  Fayaz Yusuf Khan

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

from diary import (
    application_factory, Base, create_entry, create_database_session, Entry)


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
    elif arguments['server']:
        app = application_factory()
        app.run()


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
