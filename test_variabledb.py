import os
import pytest
from variabledb  import VariableDB

TEST_DB_FILE = "test_vars.db"

@pytest.fixture
def sample_scope():
    return {}

@pytest.fixture
def clean_db(sample_scope):
    db = VariableDB(TEST_DB_FILE, scope=sample_scope)
    db.clear()
    yield db
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def test_add_and_get_variable(clean_db):
    x = 100
    clean_db.add(x, name="x_val")
    assert clean_db["x_val"] == 100

def test_get_with_default(clean_db):
    assert clean_db.get("missing", default="not found") == "not found"

def test_add_multiple(clean_db):
    clean_db.add_multiple(a=1, b=2)
    assert clean_db["a"] == 1
    assert clean_db["b"] == 2

def test_delete_variable(clean_db):
    clean_db.add(123, name="temp")
    clean_db.delete("temp")
    assert "temp" not in clean_db

def test_update_variables(clean_db):
    clean_db.add_multiple(a=1)
    clean_db.update({"a": 999, "b": 2})
    assert clean_db["a"] == 999
    assert clean_db["b"] == 2

def test_update_no_overwrite(clean_db):
    clean_db.add_multiple(a=1)
    clean_db.update({"a": 999, "b": 2}, overwrite=False)
    assert clean_db["a"] == 1  # Should NOT overwrite
    assert clean_db["b"] == 2  # Should be added

def test_save_and_load(sample_scope):
    db = VariableDB(TEST_DB_FILE, scope=sample_scope)
    db.add("hello", name="greeting")
    db.save()

    new_db = VariableDB(TEST_DB_FILE, scope=sample_scope)
    new_db.load()
    assert new_db["greeting"] == "hello"
    assert "greeting" in sample_scope  # Scope should be updated

    os.remove(TEST_DB_FILE)
