import tomllib as toml
from typing import Optional, NamedTuple, Type, TypeVar, IO, cast

#reads toml files allows for setting the given directory of the aforementioned toml file as well
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

#TODO: Replace with the new syntax once supported by mypy
T=TypeVar("T", bound="Config")#Manual Type needed for Singleton 

#Singleton Only one config can exist
class Config():
    """
    Creates a Singleton object for the config file as only one config file can exist. 
    Returns the config as a dictionary.
    """
    _instance = None
    
    def __new__(cls: Type[T], filepath: str) -> T:
        """Enforces the Singleton Design Pattern"""
        if cls._instance is None:
            cls._instance= super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, filepath: str="") -> None:
        self.filepath = str(filepath)
        self.tml=self.ConfParse()

    class Ingest(NamedTuple):
        """
        Subclass of Config that defines a NamedTuple which is used for returning the values for the config.
        """
        logging: bool
        safetyPrompt: bool
        loginFilesDir: str #forward reference

    def ConfParse(self) -> Ingest:
        """
        Ingests the configuration file and stores the variables, it is then output as a Ingest Named tuple. 
        """
        ConfigVars=["LoginFilesDir", "PromptForSafety", "Logging"]
        tml=TOMLRead(self.filepath)
        if all(x in ConfigVars for x in tml):
            self.tml= self.Ingest(logging=tml["Logging"], loginFilesDir=tml["LoginFilesDir"], safetyPrompt=tml["PromptForSafety"])
            return(self.tml)
        else:
            raise ValueError("Error, your CONFIG is MALFORMED")
            


class Action(NamedTuple):
    """
    A data structure representing an action to be performed in Login Files Used by TOMLparser, 

    Attributes
    ----------
    type : str
        The type of action (e.g., 'wait', 'text', 'click', 'move').
    id : dict, optional
        The identifiers for the action, relevant for all types except 'wait'.
    value : dict, optional
        The values associated with the action, used for all wait and text actions.
        Including Keyring Activation and Storage type. 
    """
    #type of action
    type: str
    #value is not used by wait actions
    id: Optional[dict] = None    
    #value is only used by text actions
    value: Optional[dict] = None
