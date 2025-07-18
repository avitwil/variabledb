import pytest
from variabledb import VariableDB

def test_add_without_name_and_scope_fails():
    val = 123
    db = VariableDB("test.db", scope={})
    with pytest.raises(ValueError, match="Cannot determine variable name"):
        db.add(val)  # No scope match, no name

def test_delete_non_existing_variable():
    db = VariableDB("test.db", scope={})
    with pytest.raises(KeyError):
        db.delete("non_existent")

def test_delete_with_invalid_key_type():
    db = VariableDB("test.db", scope={})
    with pytest.raises(ValueError):
        db.delete(123)  # Not a string