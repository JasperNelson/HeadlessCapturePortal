from __future__ import annotations
from Captr.TOMLRead import TOMLRead
from typing import NamedTuple, Type, IO, cast
import os

#reads toml files allows for setting the given directory of the aforementioned toml file as well
#TODO: Replace with the new syntax once supported by mypy
 

#Singleton Only one config can exist
class Config():
    """
    Creates a Singleton object for the config file as only one config file can exist. 
    Returns the config as a dictionary. Takes a string as the location of the config file 
    Unless if the environment variable CAPTURE_CONFIG is set in which it is manually overrided to such. 
    """
    _instance: 'Config' | None = None
    
    def __new__(cls: Type['Config'], filepath: str | IO[bytes]) -> 'Config':
        """Enforces the Singleton Design Pattern"""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, filepath: str = "") -> None:
        if Type is IO[bytes]:
            self.filepath = filepath
        else:  
            if os.environ.get("CAPTURE_CONFIG") is not None:
                self.filepath = cast(str, os.environ.get("CAPTURE_CONFIG"))
            elif filepath != "":
                self.filepath = str(filepath)
            else:
                raise ValueError('Neither a supplied config dir or a environment variable CAPTURE_CONFIG could be found'
                                 )
        self.export = self.ConfParse()

    class _ingest(NamedTuple):
        """
        Subclass of Config that defines a NamedTuple which is used for returning the values for the config.
        """
        logging: bool
        safetyPrompt: bool
        loginFilesDir: str  # forward reference
        defaultBackend: str
        keyringBackend: str

    def ConfParse(self) -> _ingest:
        """
        Ingests the configuration file and stores the variables, it is then output as a Ingest Named tuple. 
        """
        ConfigVars = ["LoginFilesDir", "PromptForSafety", "Logging", "DefaultBackend", "KeyringBackend"] 
        tml = TOMLRead(self.filepath)
        if all(x in ConfigVars for x in tml):
            self.export = self._ingest(logging=tml["Logging"], loginFilesDir=tml["LoginFilesDir"], 
                                       safetyPrompt=tml["PromptForSafety"], defaultBackend=tml["DefaultBackend"], 
                                       keyringBackend=tml["KeyringBackend"])
            return (self.export)
        else:
            raise ValueError("Error, your CONFIG is MALFORMED")
