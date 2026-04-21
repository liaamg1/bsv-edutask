import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

def test_get_user_by_email_user_not_found ():
    """None existing email returns nothing"""
    mock_dao = Mock()
    mock_dao.find.return_value = [] # No user found
    user_controller = UserController(mock_dao)
    result = user_controller.get_user_by_email("local-part@domain.host")

    assert result is None

def test_get_user_by_email_many_users_found (capsys):
    """Many of the same emails returns user, and warning"""
    mock_dao = Mock()
    mock_dao.find.return_value = [
        {"email": "local-part@domain.host"}, 
        {"email": "local-part@domain.host"}
    ] # multiple users found

    user_controller = UserController(mock_dao)
    result = user_controller.get_user_by_email("local-part@domain.host")
    captured = capsys.readouterr()

    assert result["email"]=="local-part@domain.host"
    assert "Error: more than one user found with mail local-part@domain.host" in captured.out
def test_get_user_by_email_valid_single_user_returns_user():
    """Valid user email exists and returns user"""
    mock_dao=Mock()
    mock_dao.find.return_value = [{"email": "valid@email.com"}]

    controller = UserController(mock_dao)

    result = controller.get_user_by_email("valid@email.com")
    
    assert result["email"]=="valid@email.com"

def test_get_user_by_email_invalid_single_user_returns_error():
    """Invalid email and returns error"""
    mock_dao=Mock()

    controller = UserController(mock_dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalidEmail")
