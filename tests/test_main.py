import sys
from unittest.mock import patch

from diary import main


@patch('diary.cli.docopt', return_value={'<file>': 'test.db', 'show': True})
@patch('diary.cli.getpass', return_value='password')
@patch('diary.cli.create_database_session')
@patch('diary.cli.show')
def test_main_show(show, create_database_session, *_):
    session = create_database_session.return_value
    main()
    create_database_session.assert_called_once_with('test.db', 'password')
    show.assert_called_once_with(session)


@patch('diary.cli.docopt', return_value={
    '<file>': 'test.db', 'show': False,
    'write': True, '--create': False, '--message': None})
@patch('diary.cli.getpass', return_value='password')
@patch('diary.cli.create_database_session')
@patch('diary.cli.write_from_buffer')
def test_main_write_from_buffer(write_from_buffer,
                                create_database_session, *_):
    session = create_database_session.return_value
    main()
    write_from_buffer.assert_called_once_with(session, sys.stdin)
