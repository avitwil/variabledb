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
    """Ensure the filename has a .db extension.

    Args:
        filename: The name of the file to check.

    Returns:
        The filename with .db extension added if it was missing.

    Raises:
        TypeError: If filename is not a string.

    Example:
         check_file_name("data")

         check_file_name("data.db")

    """
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    return filename if filename.endswith(".db") else f"{filename}.db"

class VariableDb:
    """A class to manage a dictionary of variables stored in a .db file.

    The class allows adding, deleting, replacing, saving, and loading variables
    to/from a file using pickle, with variable names resolved from a given scope.

    Attributes:
        filename: The name of the file to save/load variables (with .db extension).
        data: The dictionary storing variable names and values.
        scope: The dictionary used to resolve variable names (e.g., globals()).
    """
    unsaved_files = []
    def __init__(self, filename: str, scope: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the VariableDb with a filename and optional scope.

        Args:
            filename: The name of the file to save/load variables.
            scope: The dictionary to resolve variable names. Defaults to globals().

        Raises:
            TypeError: If filename is not a string or scope is not a dictionary.

        Example:
             db = VariableDb("data",globals())

             db = VariableDb("data.db",locals())

        """
        self.filename: str = check_file_name(filename)
        self.data: Dict[str, Any] = {}
        self.scope: Dict[str, Any] = scope if scope is not None else globals()
        if not isinstance(self.scope, dict):
            raise TypeError("scope must be a dictionary")
        VariableDb.unsaved_files.append(self.filename)

    def __enter__(self):
        """Enter the context, loading variables from the file if it exists.

             Checks if the file specified by `filename` exists. If it does, calls the
             `load` method to populate the internal dictionary (`self.data`) with the
             variables stored in the file. If the file does not exist, the dictionary
             remains empty. Returns the `VariableDb` instance to allow operations within
             the context.

             Returns:
                 VariableDb: The current instance of the VariableDb class.

             Raises:
                 FileNotFoundError: If the file exists but cannot be accessed.
                 pickle.UnpicklingError: If deserialization of the file fails.
                 ValueError: If the loaded data is not a dictionary.

             Example:

                  with VariableDb("data") as db:

                 # Automatically saves to 'data.db' on context exit
             """
        try:
            if not os.path.exists(self.filename):
                self.add_to_unsaved()
                return self
            else:
                self.load()
                return self
        except Exception as e:
            logging.error(f"Failed to save on context exit: {e}")

    def __repr__(self):
        return f"VariableDb(filename={self.filename},scope={self.scope})"

    def __len__(self):
        return len(self.data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context, saving the variables dictionary to the file.

        Calls the `save` method to persist the current state of the internal
        dictionary (`self.data`) to the file specified by `filename`. This ensures
        that any changes made to the dictionary during the context are saved
        automatically. Errors during saving are logged but do not interrupt the
        program.

        Args:
            exc_type: The type of the exception that occurred, if any.
            exc_val: The instance of the exception that occurred, if any.
            exc_tb: The traceback of the exception that occurred, if any.

        Raises:
            OSError: If there is an error writing to the file.
            pickle.PicklingError: If serialization fails.

        Example:
            
             with VariableDb("data") as db:
            
            # Automatically saves {'x': 42} to 'data.db' on exit
        """

        try:
            self.save()
        except Exception as e:
            logging.error(f"Failed to save on context exit: {e}")

    def get_variable_name(self, variable: Any) -> Optional[str]:
        """Retrieve the name of a variable from the scope.

        Args:
            variable: The variable object to find in the scope.

        Returns:
            The name of the variable if found, otherwise None.

        Example:

             x = 42

             db.get_variable_name(x) --> 'x'

        """
        try:
            for name, val in self.scope.items():
                if val is variable:
                    return name
        except (KeyError, TypeError) as e:
            logging.warning(f"Failed to get variable name: {e}")
        return None

    def add(self, variable: Any) -> None:
        """Add a variable to the dictionary if it doesn't already exist.

        Args:
            variable: The variable to add.

        Raises:
            ValueError: If the variable name cannot be determined.
            KeyError: If the variable name already exists in the dictionary.

        Example:

             x = 42

            db.add(x)

        """
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

    def add_multiple(self, *variables: Any ) -> None:
        """Add multiple variables to the dictionary.

        Args:
            *variables: One or more variable objects to add.

        Raises:
            ValueError: If any variable name cannot be determined.
            KeyError: If any variable name already exists in the dictionary.

        Example:

             x, y = 42, "test"

             db.add_multiple(x, y)

        """
        try:
            for variable in variables:
                self.add(variable)
            self.add_to_unsaved()
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f"Failed to add multiple variables: {e}")

    def delete(self, variable: Any) -> None:
        """Delete a variable from the dictionary based on its value.

        Args:
            variable: The variable to remove (resolved by identity).

        Raises:
            ValueError: If the variable name cannot be determined.
            KeyError: If the variable name is not found in the dictionary.

        Example:

             db.delete(x)

        """
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
        """Replace the value of an existing variable in the dictionary.

        Args:
            variable: The variable with the new value to replace.

        Raises:
            ValueError: If the variable name cannot be determined.
            KeyError: If the variable name does not exist in the dictionary.

        Example:

             db.replace(x)

        """
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
        """Save the variables dictionary to the specified .db file using pickle.

        Raises:
            OSError: If there is an error writing to the file.
            pickle.PicklingError: If serialization fails.

        Example:

             db.save()

        """
        try:
            with open(self.filename, "wb") as file:
                pickle.dump(self.data, file)
                if self.filename in VariableDb.unsaved_files:
                    VariableDb.unsaved_files.remove(self.filename)
        except (OSError, pickle.PicklingError) as e:
            logging.error(f"Failed to save to {self.filename}: {e}")

    def load(self) -> Optional[List[str]]:
        """Load variables from the .db file into the dictionary .

        Updates the internal dictionary  with the loaded variables.

        Raises:
            FileNotFoundError: If the file does not exist.
            pickle.UnpicklingError: If deserialization fails.
            ValueError: If the loaded data is not a dictionary.

        Example:

             db.load()

        Extra:

        to add values to globals() or locals() add this line

        globals().update(<self>.data)

        -or-

        locals().update(<self>.data)



        """
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
        """Clear all variables from the dictionary.

        Example:

             db.clear()

        """
        self.data.clear()
        self.add_to_unsaved()

    def print(self):
        for i in self.data:
            print(f"{i} = {self.data[i]}")

    def add_to_unsaved(self):
        if self.filename not in VariableDb.unsaved_files:
            VariableDb.unsaved_files.append(self.filename)

def save_all_open_files():
    for i in VariableDb.unsaved_files:
        with VariableDb(i) as file:
            file.save()