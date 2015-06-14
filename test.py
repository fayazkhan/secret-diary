from mock import Mock

from diary import show


def test_show():
    show(session)
    print.assert_called_once_with(humanized_time, content)
