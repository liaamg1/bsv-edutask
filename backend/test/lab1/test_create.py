import pytest
from unittest.mock import Mock
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
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_database"]
    collection = "users_test"

    db.drop_collection(collection)

    db.create_collection(collection, validator=VALIDATOR)

    with patch("src.util.dao.getValidator", return_value=VALIDATOR):
        dao = DAO(collection)

    yield dao

    db.drop_collection(collection)
    client.close()