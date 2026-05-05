import pytest
from unittest.mock import patch
from pymongo import MongoClient
from pymongo.errors import WriteError

from src.util.dao import DAO

VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"bsonType": "string"},
            "email": {
                "bsonType": "string", 
                "uniqueItems": True
            }
        }
    }
}

@pytest.fixture
def dao():
    client = MongoClient("mongodb://root:root@localhost:27017")
    db = client["test_database"]
    collection = "users_test"

    if collection in db.list_collection_names():
        db.drop_collection(collection)

    db.create_collection(collection, validator=VALIDATOR)
    db[collection].create_index("email", unique=True)

    with patch("src.util.dao.getValidator", return_value=VALIDATOR):
        dao_instance = DAO(collection)

    yield dao_instance

    db.drop_collection(collection)
    client.close()

@pytest.mark.integration
def test_create_valid_returns_inserted_document(dao):
    """Data compliant to the validator returns the object parsed to JSON with an _id attribute."""
    data = {"name": "123", "email": "local-part@domain.host"}

    result = dao.create(data)

    assert result == {
        "name": data["name"],
        "email": data["email"],
        "_id": result["_id"]
    }

@pytest.mark.integration
def test_create_missing_required_field(dao):
    """Data missing required field raises WriteError."""
    data = {"name": "Alice"}

    with pytest.raises(WriteError):
        dao.create(data)
        
@pytest.mark.integration
def test_create_type_invalid(dao):
    """Data containing the wrong data type raises WriteError"""
    data = {"name": 123,"email":"local-part@domain.host"}

    with pytest.raises(WriteError):
        dao.create(data)

@pytest.mark.integration
def test_create_not_unique_email(dao):
    """Data is not unique and raises WriteError"""
    data = {"name": "123","email":"local-part@domain.host"}

    dao.create(data)

    with pytest.raises(WriteError):
        dao.create(data)