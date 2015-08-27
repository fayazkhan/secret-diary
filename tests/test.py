from unittest.mock import Mock, patch

import arrow

from diary import create_entry, Entry, show, write_from_buffer


def test_show():
    content = 'test'
    time = arrow.now()
    session = Mock(query=Mock(return_value=[Entry(
        updated=time, content=content)]))
    with patch('diary.display_row') as display_row:
        show(session)
    display_row.assert_called_once_with(time.humanize(), content)


def test_create_entry():
    session = Mock()
    entry = create_entry(session, message='test')
    session.add.assert_called_once_with(entry)
    session.commit.assert_called_once_with()
    assert entry.content == 'test'


def test_write_from_buffer():
    session = Mock()
    buffer = ['hello', 'world']
    entry = Entry()
    with patch('diary.create_entry', return_value=entry):
        write_from_buffer(session, buffer)
    assert entry.content == 'helloworld'
