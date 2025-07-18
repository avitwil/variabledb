import dill
import logging
import os
from typing import Any, Optional, Iterator, Tuple, Dict

logging.basicConfig(
    level=logging.DEBUG,
    filename='variabledb_log.log',
    encoding='utf-8',
    filemode='w',
    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])',
    datefmt='%d/%m/%y %I:%M:%S'
)
logger = logging.getLogger(__name__)

class File:
    """
    Descriptor for validating and formatting filenames.
    Ensures the filename is a string and ends with '.db'.
    """

    def __init__(self) -> None:
        self.name: Optional[str] = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: Any, owner: type) -> Optional[str]:
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance: Any, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"{self.name} must be a string")
        instance.__dict__[self.name] = value if value.endswith(".db") else f"{value}.db"


class VariableDB:
    """
    A simple variable-based database using dill for persistence.
    Stores variables by name, allows loading and saving to a file.

    Attributes:
        filename (str): The path to the .db file.
        scope (dict): The external scope to bind variables into.
        data (dict): The actual stored data.
    """

    filename = File()

    def __init__(self, filename: str, *, scope: Dict[str, Any], data: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the VariableDB.

        Args:
            filename (str): The file to save/load from.
            scope (dict): A namespace (usually globals()) for variable resolution.
            data (dict, optional): Initial data to populate the database.
        """
        self.filename = filename
        self.data = data or {}
        self.scope = scope

    def __repr__(self) -> str:
        return f"VariableDB(filename={self.filename!r}, data_keys={list(self.data.keys())})"

    def __str__(self) -> str:
        lines = [f"VariableDB: {self.filename}"]
        if not self.data:
            lines.append("  (empty)")
        else:
            for key, value in self.data.items():
                lines.append(f"  - {key}: {type(value).__name__} = {repr(value)}")
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self.data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VariableDB):
            return NotImplemented
        return self.data == other.data and self.filename == other.filename

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """
        Iterate over (key, value) pairs in the database.
        """
        return iter(self.data.items())

    def __delitem__(self, key: str) -> None:
        """
        Delete an item by key.

        Args:
            key (str): The key to delete.
        """
        del self.data[key]

    def __bool__(self) -> bool:
        """
        Return True if database contains any data, else False.
        """
        return bool(self.data)

    def __enter__(self) -> "VariableDB":
        """
        Context manager entry: loads data from file.

        Returns:
            VariableDB: The instance itself.
        """
        try:
            self.load()
        except Exception as e:
            logger.error(f"(VariableDB.__enter__) {e}")
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """
        Context manager exit: saves data to file.
        """
        try:
            self.save()
        except Exception as e:
            logger.error(f"(VariableDB.__exit__) {e}")

    def __getitem__(self, key: str) -> Any:
        """
        Get an item by key.

        Args:
            key (str): The key to retrieve.

        Returns:
            Any: The value stored under the key.
        """
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set an item by key.

        Args:
            key (str): The key under which to store the value.
            value (Any): The value to store.
        """
        self.data[key] = value

    def __contains__(self, key: str) -> bool:
        """
        Check if a key exists in the database.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if key exists, False otherwise.
        """
        return key in self.data

    def get_variable_name(self, variable: Any) -> Optional[str]:
        """
        Attempt to retrieve the variable's name from the scope.

        Args:
            variable (Any): The variable to look up.

        Returns:
            Optional[str]: The name of the variable in the scope, if found.
        """
        try:
            for name, val in self.scope.items():
                if val is variable:
                    return name
        except Exception as e:
            logger.error(f"(VariableDB.get_variable_name) {e}")
        return None

    def add(self, variable: Any, name: Optional[str] = None) -> None:
        """
        Add a single variable to the database.

        Args:
            variable (Any): The variable to store.
            name (Optional[str]): The name to store it under. If None, tries to infer from scope.

        Raises:
            ValueError: If the name can't be determined.
        """
        if name is None:
            name = self.get_variable_name(variable)
        if name is None:
            raise ValueError("Cannot determine variable name to add")
        self.data[name] = variable

    def add_multiple(self, **variables: Any) -> None:
        """
        Add multiple variables at once.

        Args:
            **variables: Variables to add, with names as keys.
        """
        try:
            for name, variable in variables.items():
                self.add(variable, name)
        except Exception as e:
            logger.error(f"(VariableDB.add_multiple) {e}")

    def delete(self, variable_name: str) -> None:
        """
        Delete a variable from the database by name.

        Args:
            variable_name (str): The name of the variable to delete.

        Raises:
            ValueError: If variable_name is not a string.
            KeyError: If variable_name does not exist in data.
        """
        try:
            if not isinstance(variable_name, str):
                raise ValueError("variable name must be string")
            elif variable_name not in self.data:
                raise KeyError(f"Variable '{variable_name}' not found in database")
            else:
                del self.data[variable_name]
        except Exception as e:
            logger.error(f"(VariableDB.delete) {e}")

    def clear(self) -> None:
        """
        Clear all stored variables.
        """
        self.data.clear()

    def save(self) -> None:
        """
        Save the data to the file using dill.
        """
        try:
            folder = os.path.dirname(self.filename)
            if folder and not os.path.exists(folder):
                os.makedirs(folder)
            with open(self.filename, "wb") as file:
                dill.dump(self.data, file)
        except Exception as e:
            logger.error(f"(VariableDB.save) {e}")

    def load(self) -> None:
        """
        Load the data from the file using dill.
        Updates the given scope if loading succeeds.
        """
        try:
            with open(self.filename, "rb") as file:
                self.data = dill.load(file)
                if self.data is not None:
                    self.scope.update(self.data)
        except FileNotFoundError:
            pass
        except Exception as e:
            logger.error(f"(VariableDB.load) {e}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve a value by key, return default if key not found.

        Args:
            key (str): The key to look up.
            default (Any, optional): Value to return if key is not found.

        Returns:
            Any: The value stored under key or default.
        """
        return self.data.get(key, default)
