#orchestrates the project
import argparse
import os
from tomllib import TOMLDecodeError
#from Captr.logging import logging
from Captr.ConfigParser import Config
from Captr.LoginParser import LoginParser, Action
from Captr.backend import backend
from Captr.Debackend import DebugBackend
from Captr.SimpleBackend import SimpleBackend
import logging
from typing import NamedTuple


class Orchestrator(): 
    def __init__(self, modes: argparse.Namespace):
        #prep
        #print(vars(modes))
        self.logger=logging.getLogger(__name__)
        self.logger.debug(f"source modes={modes}")
        self.modes=self._namespaceToModes(modes)
        self.logger.debug(f"parsed modes={self.modes}")
        self.backends={"Debug":DebugBackend, "Simple": SimpleBackend}
        self.config=Config("./CONFIG.toml")
        self.logger.debug(f"Config Vars={self.config.export}")
        self.defaultBackend=self.config.export.defaultBackend
        self.loginFilesDir=self.config.export.loginFilesDir
    #     print(self.defaultBackend)
        #start parsing options and split
        self.relay()


    def _namespaceToModes(self, modes: argparse.Namespace) -> dict:
        """
        Internal method in Orchestrator that maps argparse.Namespace to a more consistant dictionary interface
        where False = the option was not used
        """
        result: dict ={}
        result["verbose"]=modes.verbose if modes.verbose is not None else False
        result["Remove"]=modes.Remove if modes.Remove is not None else False
        result["URL"]=modes.URL if modes.URL is not None else False
        result["Layout"]=modes.Layout if modes.Layout is not None else False
        result["Auto"]=modes.Auto if modes.Auto != '' else False
        result["yes"]=modes.yes if modes.yes is not None else False
        result["default"]=modes.default if modes.default is not None else False

        return result

    def _backendCheck(self, name: str) -> None:
        """
        internal method of Orchestrator, used exclusively by backendBuilder
        to see if the supplied backend is a backend listed in compatable backends
        """
        if name not in self.backends.keys():
            raise ValueError(f"Bad backend: '{name}'")
        
    def _backendBuilder(self, backendOverride : None | str = None) -> backend:
        """
        internal method of Orchestrator, returns a useable backend object
        """
        #the flag used to identify the backend
        bFlag: str
        #the backend object
        backedobj: backend
        if backendOverride is not None:
            bFlag=backendOverride
        else: bFlag=self.defaultBackend
        self._backendCheck(bFlag)
        backedobj=self.backends[bFlag]()
        
       # print(backedobj)
        return backedobj
    def _Reader(self, filepath: str) -> LoginParser._ingest:
        """
        Internal method of Orchestrator, 
        Purpose: to take a filepath and use LoginParse to return a LoginParser._ingest NamedTuple
        """
        parsedOb=LoginParser(filepath)
        ingest=parsedOb.export
        assert isinstance(ingest, LoginParser._ingest)
        return(ingest)
    
    def _Remove(self) -> None:
        #TODO: Doesnt use a backend as it uses keystorer instead
        pass


    def _Auto(self, path: str) -> None:
        if not os.path.exists(path):
            raise OSError(f"Error, The path [{path}] is invalid, or permissions dont permit access")
        #try to filter out some of the junk that may inevitably enter the directory
        loginfiles=(loginfiles for loginfiles in os.listdir(path) if loginfiles.endswith(".toml")) 
        for lFile in loginfiles:
            try:
                self._Reader(path+"/"+lFile)
            except TOMLDecodeError as de:
                self.logger.warn(f"The file {lFile} has a invalid toml format \n skipping ...")
            except UnicodeDecodeError as ude:
                self.logger.warn(f"The file {lFile} appears to be corrupted \n skipping ...")
            except ValueError as ve:
                self.logger.warn(f"Something was wrong with the formatting of the toml file {lFile}, Error = {ve} \n skipping ...")
            except PermissionError as pe:
                self.logger.warn(f"Permissions do not allow reading the file {lFile} \n skipping ...")
            except Exception as e: 
                self.logger.error(f"Unknown error: {str(e)} \n skipping ...")
            #next design a function that relegates actions etc. #and one that reads the url and compares it to the captive portal url

    def _URL(self) -> None:
        self._backendBuilder()
    def _Layout(self) -> None:
        self._backendBuilder()
    def _default(self) -> None:
        filepath=self.modes["default"]
        try:
            session=LoginParser(filepath)
        except OSError:
            raise OSError(f"Error, the filepath is invalid or permissions dont permit read access")
        
        self._backendBuilder()
    def relay(self) -> None:
        """
        Function of orchestrator that parses arguments and activates the appropriate member functions. 

        Arguments: 
        None
        """
        #temp for testing
       
        if self.modes["verbose"]==True:
            pass
        if self.modes["Remove"]!=False:
            self._Remove()
        elif self.modes["Auto"]!=False:
            if self.modes["Auto"] is None:
                self._Auto(self.loginFilesDir)
            else: #If there was a directory redirect supplied
                self._Auto(self.modes["Auto"])
        elif self.modes["URL"]!=False:
            self._URL()
        elif self.modes["Layout"]!=False:
            self._Layout()
        else:
            self._default()
       

