#orchestrates the project
import argparse
import os
#from Captr.logging import logging
from Captr.ConfigParser import Config
from Captr.LoginParser import LoginParser, Action
from Captr.backend import backend
from Captr.Debackend import DebugBackend
from Captr.SimpleBackend import SimpleBackend
import logging
from typing import NamedTuple
logger=logging.getLogger(__name__)


class Orchestrator(): 
    def __init__(self, modes: argparse.Namespace):
        #prep
        logger.warning(f"modes={[e for e in self._namespaceToModes(modes).items()]}")
        self.modes=modes
        # print(vars(modes))
        self.backends={"Debug":DebugBackend, "Simple": SimpleBackend}
        self.config=Config("./CONFIG.toml")
        self.defaultBackend=self.config.export.defaultBackend
        self.loginFilesDir=self.config.export.loginFilesDir
    #     print(self.defaultBackend)
        #start parsing options and split
        self.relay()
    def _namespaceToModes(self, modes: argparse.Namespace) -> dict:
        result: dict ={}
        result["verbose"]=modes.verbose if modes.verbose is not None else False
        return result

    def _backendCheck(self, name: str) -> None:
        if name not in self.backends.keys():
            raise ValueError(f"Bad backend: '{name}'")
        
    def backendBuilder(self, backendOverride : None | str = None) -> backend:
        bFlag: str
        backedobj: backend
        if backendOverride is not None:
            bFlag=backendOverride
        else: bFlag=self.defaultBackend
        self._backendCheck(bFlag)
        backedobj=self.backends[bFlag]()
        
       # print(backedobj)
        return backedobj

    def _Remove(self) -> None:
        pass
    def _Auto(self, path: str) -> None:
        if not os.path.exists(path):
            raise OSError(f"Error, The path [{path}] is invalid, or permissions dont permit access")
    def _URL(self) -> None:
        self.backendBuilder()
    def _Layout(self) -> None:
        self.backendBuilder()
    def _default(self) -> None:
        filepath=str("./EXAMPLE.toml")
        try:
            session=LoginParser(filepath)
        except:
            pass
        self.backendBuilder()
    def relay(self) -> None:
        """
        Function of orchestrator that parses arguments and activates the appropriate member functions. 

        Arguments: 
        None
        """
        #temp for testing
       
        if self.modes.verbose==True:
            pass
        if self.modes.Remove!=None:
            self._Remove()
        elif self.modes.Auto!='':
            if self.modes.Auto is None:
                self._Auto(self.loginFilesDir)
            else: #If there was a directory redirect supplied
                self._Auto(self.modes.Auto)
        elif self.modes.URL!=False:
            self._URL()
        elif self.modes.Layout!=[]:
            self._Layout()
        else:
            pass


