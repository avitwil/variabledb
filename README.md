

# VariableDB

VariableDB is a lightweight variable-based persistence system built with `dill`. It allows you to save, load, and manage Python variables in a `.db` file using an intuitive API. It's designed for simplicity, flexibility, and integration into scripts or small applications.

## Features

- Store and retrieve Python variables by name.
- Use context manager support (`with` statement) for automatic loading and saving.
- Infer variable names from a given scope (e.g., `globals()`).
- Add variables individually or in bulk.
- Supports custom filenames (automatically ensures `.db` extension).
- Uses `dill` for serialization (supports more Python objects than `pickle`).
- Built-in logging to track operations and errors.

## Installation

No external installation is required beyond `dill`. Install it with:

```bash
pip install dill
````

## Usage

```python
from variabledb import VariableDB

x = 42
y = [1, 2, 3]
scope = globals()

with VariableDB("my_vars", scope=scope) as db:
    db.add(x)
    db.add(y, name="my_list")
    db.save()

# Later, to load the variables:
with VariableDB("my_vars", scope=globals()) as db:
    print(db["x"])       # 42
    print(db["my_list"]) # [1, 2, 3]
```

## Class: VariableDB

### Constructor

```python
VariableDB(filename: str, *, scope: dict, data: dict = None)
```

* `filename`: Name of the `.db` file (`.db` extension is added if missing).
* `scope`: The variable scope (e.g., `globals()` or `locals()`) used to bind variables.
* `data`: Optional dictionary of initial data.

### Key Methods

* `add(variable, name=None)`
  Adds a single variable. If `name` is not given, it tries to infer it from the scope.

* `add_multiple(**variables)`
  Adds multiple variables at once.

* `get(key, default=None)`
  Gets a variable by name, returns `default` if not found.

* `delete(variable_name)`
  Deletes a variable by name.

* `clear()`
  Clears all stored variables.

* `save()`
  Saves data to the file using `dill`.

* `load()`
  Loads data from the file and updates the provided scope.

* `update(variables, overwrite=True)`
  Updates the database with a dictionary of variables. Set `overwrite=False` to preserve existing data.

### Magic Methods

* `__getitem__`, `__setitem__`: Indexing support (`db['x'] = 42`)
* `__enter__`, `__exit__`: Context manager for automatic load/save
* `__iter__`: Iterate over stored key-value pairs
* `__len__`, `__bool__`: Check if database is empty or get number of variables
* `__str__`, `__repr__`: Readable string representations

## Logging

Logging is configured to write to `variabledb_log.log` in the working directory. It includes timestamps, line numbers, and message severity for better traceability and debugging.

## License

This project is provided as-is. You are free to use, modify, and distribute it for personal or commercial purposes.

## Author

Avi Twil

