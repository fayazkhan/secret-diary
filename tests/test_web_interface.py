from unittest.mock import patch

from diary.web import application_factory


@patch('diary.web.Flask')
def test_webapp_initialization(Flask):
    application_factory()
    Flask.assert_called_once_with('diary.web')


@patch('diary.web.Admin')
def test_admin_initialzed(Admin):
    app = application_factory()
    Admin.assert_called_once_with(app)
