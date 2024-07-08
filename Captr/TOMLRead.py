import tomllib as toml
from typing import IO, cast

def TOMLRead(f: IO[bytes] | str) -> dict:
    """
    Simple function that Opens Toml Files saves them to a variable and then returns whats in them

    Arguments:
    - f: Either a string representing a filename, or a file-like, such as the values returned by
         Python's io.ButesIO() or open(foo, "rb") builtin
    Returns:
        Returns a parsed TOML object.
    """
    tml: dict
    try:
        if type(f) == str:
            with open(f, "rb") as inputFile:
                 tml=toml.load(inputFile)
        else:
            tml = toml.load(cast(IO[bytes], f))
    except UnicodeDecodeError as err:
        print("ERROR: Your TOML File Appears to be corrupted or your pointing to the wrong file")
        raise err
    except toml.TOMLDecodeError:
        raise toml.TOMLDecodeError("Your TOML File Appears to have Formatting Errors")
    except FileNotFoundError:
        raise FileNotFoundError("Cannot Find the File, Ensure the file path is correct and the file exits")
    except PermissionError:
            raise PermissionError("Unable to reach the file due to Permission")          
    return tml