import tomllib as toml
from typing import Optional, NamedTuple, Any, Type, TypeVar, IO, cast

def TOMLRead(f: IO[bytes] | str) -> dict:
    """
    Simple function that Opens Toml Files saves them to a variable and then returns whats in them

    Arguments:
    - f: Either a string representing a filename, or a file-like, such as the values returned by
         Python's io.ButesIO() or open(foo, "rb") builtin
    Returns:
        Returns a parsed TOML object.
    """
    inputFile: IO[bytes] | str
    if type(f) == str:
        inputFile = cast(IO[bytes], open(cast(str, f), "rb"))
    else:
        inputFile = cast(IO[bytes], f)

    with inputFile:
        try:
            tml = toml.load(inputFile)
        except UnicodeDecodeError as err:
            print("ERROR: Your TOML File Appears to be corrupted or your pointing to the wrong file")
            raise err
        except toml.TOMLDecodeError:
            raise toml.TOMLDecodeError("Your TOML File Appears to have Formatting Errors")
        except FileNotFoundError:
            raise FileNotFoundError("Cannot Find the File, Ensure the file path is correct and the file exits")    
    return tml