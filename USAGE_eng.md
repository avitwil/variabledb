

# VariableDB – Usage Guide

## Overview

`VariableDB` is a lightweight Python utility for storing, loading, and managing Python variables via a `.db` file using the `dill` serialization library. It is ideal for quick persistence of runtime data, prototyping, notebooks, or small applications that require temporary or reusable state.

---

## Requirements

* Python 3.7+
* `dill` package:

```bash
pip install dill
```

---

## Creating a VariableDB Instance

```python
from variabledb import VariableDB

db = VariableDB("my_data", scope=globals())
```

* `filename`: The name of the file to save to or load from (".db" is appended automatically).
* `scope`: A dictionary, typically `globals()`, where loaded variables will be injected.

---

## Internals

* `data`: An internal dictionary storing variables by name.
* `scope`: The external environment (usually `globals()`) to which variables are restored on load.
* `filename`: The file path (validated to end with `.db`).

---

## Main Features

### 1. `add(variable, name=None)`

Adds a single variable to the database.

```python
x = 42
db.add(x)  # Automatically detects name "x"

db.add(x, name="my_number")  # Custom name
```

If no name is provided, the system attempts to infer it from the `scope`.

---

### 2. `add_multiple(**variables)`

Adds multiple variables at once:

```python
db.add_multiple(a=1, b=2, c=[3, 4])
```

If any variable fails to be added, a `RuntimeError` is raised listing the errors.

---

### 3. `__setitem__` and `__getitem__`

Access data like a dictionary:

```python
db["x"] = 99
print(db["x"])  # 99
```

---

### 4. `save()`

Persist the internal data to disk:

```python
db.save()
```

Creates directories if needed.

---

### 5. `load()`

Load from the `.db` file. Automatically injects data into the provided scope.

```python
db.load()
print(x)  # x is now restored
```

If the file doesn't exist, no error is raised.

---

### 6. Context Manager Support

```python
with VariableDB("my_data", scope=globals()) as db:
    db["count"] = 10
# Automatically saved when exiting the block
```

---

### 7. `delete(name: str)`

Remove a variable by name:

```python
db.delete("x")
```

Raises `KeyError` if the name does not exist.

---

### 8. `clear()`

Removes all stored variables:

```python
db.clear()
```

---

### 9. `update(variables: dict, overwrite=True)`

Update the database with multiple variables:

```python
db.update({"x": 1, "y": 2})

db.update({"x": 3}, overwrite=False)  # Will not overwrite existing "x"
```

---

### 10. `get(key, default=None)`

Safely get a variable with a fallback:

```python
value = db.get("x", default=0)
```

---

### 11. `__delitem__(key)`

Equivalent to `delete`:

```python
del db["x"]
```

---

### 12. `__contains__(key)`

Check for the presence of a variable:

```python
if "x" in db:
    print("x is stored")
```

---

### 13. `__len__()`

Returns the number of stored variables:

```python
print(len(db))
```

---

### 14. `__iter__()`

Iterate over stored variables:

```python
for name, value in db:
    print(name, value)
```

---

### 15. `__bool__()`

Returns `True` if the database is not empty:

```python
if db:
    print("DB has data")
```

---

### 16. `__str__()` and `__repr__()`

Provides readable representation of contents:

```python
print(db)
```

---

## Complete Example

```python
from variabledb import VariableDB

x = 100
name = "Alice"

with VariableDB("session", scope=globals()) as db:
    db.add(x)
    db.add(name)
    db["score"] = 9000
    db.update({"level": 5, "items": ["sword", "shield"]})

# Later on...
new_db = VariableDB("session", scope=globals())
new_db.load()

print(x)       # 100
print(score)   # 9000
```

---

## Technical Notes

* File is automatically created if it does not exist.
* Directories are created if missing.
* No error is raised if the file doesn't exist on `load()`.
* Variable names are inferred only if the variable exists in the provided `scope`.

---

## Logging

Errors and warnings are logged to `variabledb_log.log`. This includes:

* File I/O errors
* Failed serialization
* Issues with variable naming or scope

---

## License

You may freely use, extend, and distribute this module. Attribution is appreciated but not required unless otherwise specified by you.




