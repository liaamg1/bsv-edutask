import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

def test_get_user_by_email_user_not_found ():
    mock_dao = Mock()
    mock_dao.find.return_value = [] # No user found
    user_controller = UserController(mock_dao)
    result = user_controller.get_user_by_email("local-part@domain.host")

    assert result is None

def test_get_user_by_email_many_users_found ():
    mock_dao = Mock()
    mock_dao.find.return_value = [
        {"email": "local-part@domain.host"}, 
        {"email": "local-part@domain.host"}
    ] # multiple users found
    user_controller = UserController(mock_dao)
    result = user_controller.get_user_by_email("local-part@domain.host")

    assert result["email"]=="local-part@domain.host"