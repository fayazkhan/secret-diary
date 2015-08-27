from unittest.mock import patch, sentinel

from diary.web import application_factory


@patch('diary.web.Flask', return_value=sentinel.app)
def test_webapp_initialization(Flask):
    app = application_factory()
    Flask.assert_called_once_with('diary.web')
    assert app == sentinel.app


@patch('diary.web.Admin')
def test_admin_initialzed(Admin):
    app = application_factory()
    Admin.assert_called_once_with(app)
