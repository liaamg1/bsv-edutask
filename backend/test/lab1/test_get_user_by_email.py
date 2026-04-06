import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

def test_get_user_by_email_valid_single_user_returns_user():
    mock_dao=Mock()
    mock_dao.find.return_value = [{"email": "valid@email.com"}]

    controller = UserController(mock_dao)

    result = controller.get_user_by_email("valid@email.com")
    
    assert result["email"]=="valid@email.com"

def test_get_user_by_email_invalid_single_user_returns_error():
    mock_dao=Mock()

    controller = UserController(mock_dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalidEmail")
