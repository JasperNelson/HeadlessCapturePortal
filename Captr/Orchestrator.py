#orchestrates the project
import argparse
from Captr.logging import logging
from Captr.ConfigParser import Config
from Captr.LoginParser
 
class Orchestrator(): 
    def __init__(self, modes: argparse.Namespace):
        self.modes=modes
        self.config=Config("./Config.toml")
        self.relay()
    class _Remove():
        pass
    class _Auto():
        def __init__(self, config: Config.Ingest, Path: None | str = None):
            
    class _URL():
        pass
    class _Layout():
        pass
    def relay(self) -> None:
        if self.modes.verbose==True:
            #start logging
            logging()
        #dont even need to 
        if self.modes.Remove!=[]:
            pass
        elif self.modes.Auto!=False:
            
        elif self.modes.URL!=[]:
            pass
        elif self.modes.Layout!=[]:
            pass

