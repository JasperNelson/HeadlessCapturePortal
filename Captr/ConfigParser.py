from __future__ import annotations
from Captr.TOMLRead import TOMLRead
from typing import Optional, NamedTuple, Type, TypeVar, IO, cast, Generic, Type, ClassVar
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
            cls._instance= super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, filepath: str="") -> None:
        if Type==IO[bytes]:
            self.filepath=filepath
        else:  
            if os.environ.get("CAPTURE_CONFIG") != None:
                self.filepath=cast(str,os.environ.get("CAPTURE_CONFIG"))
            else:
                self.filepath = str(filepath)
        self.tml=self.ConfParse()

    class Ingest(NamedTuple):
        """
        Subclass of Config that defines a NamedTuple which is used for returning the values for the config.
        """
        logging: bool
        safetyPrompt: bool
        loginFilesDir: str #forward reference
        DetectorMode: int

    def ConfParse(self) -> Ingest:
        """
        Ingests the configuration file and stores the variables, it is then output as a Ingest Named tuple. 
        """
        ConfigVars=["LoginFilesDir", "PromptForSafety", "Logging", "PortalDetectorMode"]
        tml=TOMLRead(self.filepath)
        if all(x in ConfigVars for x in tml):
            self.tml= self.Ingest(logging=tml["Logging"], loginFilesDir=tml["LoginFilesDir"], safetyPrompt=tml["PromptForSafety"], DetectorMode=tml["PortalDetectorMode"])
            return(self.tml)
        else:
            raise ValueError("Error, your CONFIG is MALFORMED")
            


