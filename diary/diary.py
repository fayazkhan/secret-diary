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

import arrow
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
