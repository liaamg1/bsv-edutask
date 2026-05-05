import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_dao():
    return Mock()

@pytest.fixture
def user_controller(mock_dao):
    return UserController(mock_dao)

def test_get_user_by_email_user_not_found(user_controller, mock_dao):
    mock_dao.find.return_value = []

    result = user_controller.get_user_by_email("local-part@domain.host")

    assert result is None

def test_get_user_by_email_many_users_found_returns_first_user(user_controller, mock_dao):
    mock_dao.find.return_value = [
        {"email": "local-part@domain.host"},
        {"email": "local-part@domain.host"}
    ]

    result = user_controller.get_user_by_email("local-part@domain.host")

    assert result["email"] == "local-part@domain.host"

def test_get_user_by_email_many_users_found_prints_warning(user_controller, mock_dao, capsys):
    mock_dao.find.return_value = [
        {"email": "local-part@domain.host"},
        {"email": "local-part@domain.host"}
    ]

    user_controller.get_user_by_email("local-part@domain.host")
    captured = capsys.readouterr()

    assert "Error: more than one user found with mail local-part@domain.host" in captured.out

def test_get_user_by_email_valid_single_user_returns_user(user_controller, mock_dao):
    mock_dao.find.return_value = [{"email": "valid@email.com"}]

    result = user_controller.get_user_by_email("valid@email.com")

    assert result["email"] == "valid@email.com"

def test_get_user_by_email_invalid_email_raises_value_error(user_controller):
    with pytest.raises(ValueError):
        user_controller.get_user_by_email("invalidEmail")

def test_get_user_by_email_database_error_raises_exception(user_controller, mock_dao):
    mock_dao.find.side_effect = Exception("DB error")

    with pytest.raises(Exception):
        user_controller.get_user_by_email("valid@email.com")