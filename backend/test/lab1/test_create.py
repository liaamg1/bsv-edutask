import pytest
from unittest.mock import patch
from pymongo import MongoClient
from dotenv import dotenv_values
import os
from pymongo.errors import WriteError

from src.util.dao import DAO

VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"bsonType": "string"},
            "email": {"bsonType": "string"}
        }
    }
}


@pytest.fixture
def dao():
    local_url = dotenv_values('.env').get('MONGO_URL')
    mongo_url = os.environ.get('MONGO_URL', local_url) or "mongodb://localhost:27017/"
    client = MongoClient(mongo_url)
    db = client["test_database"]
    collection = "users_test"

    db.drop_collection(collection)

    db.create_collection(collection, validator=VALIDATOR)

    db[collection].create_index("email", unique=True)
    db[collection].create_index("name", unique=True)

    with patch("src.util.dao.getValidator", return_value=VALIDATOR):
        dao = DAO(collection)

    yield dao

    db.drop_collection(collection)
    client.close()

@pytest.mark.unit
def test_create_type_invalid(dao):
    """Data containing the wrong data type raises WriteError"""
    data = {"name": 123,"email":"local-part@domain.host"}

    with pytest.raises(WriteError):
        dao.create(data)

@pytest.mark.unit
def test_create_not_unique(dao):
    """Data is not unique and raises WriteError"""
    data = {"name": "123","email":"local-part@domain.host"}

    dao.create(data)

    with pytest.raises(WriteError):
        dao.create(data)