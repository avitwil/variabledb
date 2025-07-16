import dill as pickle
import logging
from typing import Dict, Any, Optional, List
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='variabledb_log.log',
    encoding='utf-8',
    filemode='w',
    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])',
    datefmt='%d/%m/%y %I:%M:%S'
)

def check_file_name(filename: str) -> str:
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    return filename if filename.endswith(".db") else f"{filename}.db"

class VariableDb:
    unsaved_files = set()

    def __init__(self, filename: str, scope: Optional[Dict[str, Any]] = None) -> None:
        self.filename: str = check_file_name(filename)
        self.data: Dict[str, Any] = {}
        self.scope: Dict[str, Any] = scope if scope is not None else globals()
        if not isinstance(self.scope, dict):
            raise TypeError("scope must be a dictionary")
        VariableDb.unsaved_files.add(self.filename)

    def __enter__(self):
        try:
            if not os.path.exists(self.filename):
                self.add_to_unsaved()
            else:
                self.load()
            return self
        except Exception as e:
            logging.error(f"Failed to load file in __enter__: {e}")
            raise

    def __repr__(self):
        return f"VariableDb(filename={self.filename}, scope={self.scope})"

    def __len__(self):
        return len(self.data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.save()
        except Exception as e:
            logging.error(f"Failed to save on context exit: {e}")

    def get_variable_name(self, variable: Any) -> Optional[str]:
        try:
            for name, val in self.scope.items():
                if val is variable:
                    return name
        except (KeyError, TypeError) as e:
            logging.warning(f"Failed to get variable name: {e}")
        return None

    def add(self, variable: Any) -> None:
        try:
            name = self.get_variable_name(variable)
            if name is None:
                raise ValueError("Could not determine variable name")
            if name in self.data:
                raise KeyError(f"Variable '{name}' already exists")
            self.data[name] = variable
            self.add_to_unsaved()
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f"Failed to add variable: {e}")

    def add_by_name(self, var_name: str) -> None:
        if var_name not in self.scope:
            logging.error(f"Variable '{var_name}' not found in scope")
            raise KeyError(f"Variable '{var_name}' not found in scope")
        if var_name in self.data:
            logging.error(f"Variable '{var_name}' already exists in data")
            raise KeyError(f"Variable '{var_name}' already exists")
        self.data[var_name] = self.scope[var_name]
        self.add_to_unsaved()

    def add_multiple(self, *variables: Any) -> None:
        try:
            for variable in variables:
                self.add(variable)
            self.add_to_unsaved()
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f"Failed to add multiple variables: {e}")

    def delete(self, variable: Any) -> None:
        try:
            name = self.get_variable_name(variable)
            if name is None:
                raise ValueError("Could not determine variable name")
            if name not in self.data:
                raise KeyError(f"Variable '{name}' not found in dictionary")
            del self.data[name]
            self.add_to_unsaved()
        except (ValueError, KeyError) as e:
            logging.error(f"Failed to delete variable: {e}")

    def replace(self, variable: Any) -> None:
        try:
            name = self.get_variable_name(variable)
            if name is None:
                raise ValueError("Could not determine variable name")
            if name not in self.data:
                raise KeyError(f"Variable '{name}' does not exist")
            self.data[name] = variable
            self.add_to_unsaved()
        except (ValueError, KeyError) as e:
            logging.error(f"Failed to replace variable: {e}")

    def save(self) -> None:
        try:
            with open(self.filename, "wb") as file:
                pickle.dump(self.data, file)
            VariableDb.unsaved_files.discard(self.filename)
        except (OSError, pickle.PicklingError) as e:
            logging.error(f"Failed to save to {self.filename}: {e}")

    def load(self) -> None:
        try:
            with open(self.filename, "rb") as file:
                data = pickle.load(file)
                if not isinstance(data, dict):
                    raise ValueError("Loaded data is not a dictionary")
                self.data = data
                self.add_to_unsaved()
        except (FileNotFoundError, pickle.UnpicklingError, ValueError) as e:
            logging.error(f"Failed to load file {self.filename}: {e}")

    def clear(self) -> None:
        self.data.clear()
        self.add_to_unsaved()

    def display(self) -> None:
        for name, val in self.data.items():
            print(f"{name} = {val}")

    def add_to_unsaved(self) -> None:
        VariableDb.unsaved_files.add(self.filename)

def save_all_open_files() -> None:
    for filename in VariableDb.unsaved_files.copy():
        with VariableDb(filename) as db:
            db.load()
            db.save()
