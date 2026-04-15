import unittest.mock as mock

import pytest
from src.util.helpers import ValidationHelper 

@pytest.mark.unit
def test_validateAge_valid():
    mockObj = mock.MagicMock()
    mockObj.get.return_value = {"age": 20}
    validationHelper = ValidationHelper(mockObj)
    result = validationHelper.validateAge("1")
    # print(result)
    assert result == 'valid'

@pytest.mark.unit
def test_validateAge_invalid():
    mockObj = mock.MagicMock()
    mockObj.get.return_value = {"age": -1}
    validationHelper = ValidationHelper(mockObj)
    result = validationHelper.validateAge("2")
    # print(result)
    assert result == 'invalid'

@pytest.mark.unit
def test_validateAge_underage():
    mockObj = mock.MagicMock()
    mockObj.get.return_value = {"age": 12}
    validationHelper = ValidationHelper(mockObj)
    result = validationHelper.validateAge("3")
    # print(result)
    assert result == 'underaged'