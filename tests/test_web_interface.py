from unittest.mock import patch, sentinel

from diary.web import application_factory


@patch('diary.web.Flask', return_value=sentinel.app)
def test_webapp_initialization(Flask):
    app = application_factory()
    Flask.assert_called_once_with('diary.web')
    assert app == sentinel.app
