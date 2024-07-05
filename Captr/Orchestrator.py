#orchestrates the project
import argparse
import os
from Captr.logging import logging
from Captr.ConfigParser import Config
from Captr.LoginParser import LoginParser, Action


class Orchestrator(): 
    def __init__(self, modes: argparse.Namespace):
        self.modes=modes
        self.config=Config("./CONFIG.toml")
        self.relay()
    def _Remove(self) -> None:
        pass
    def _Auto(self, Path: None | str = None) -> None:
        pass
    def _URL(self) -> None:
        pass
    def _Layout(self) -> None:
        pass
    def relay(self) -> None:
        if self.modes.verbose==True:
            #start logging
            logging()
        #dont even need to 
        if self.modes.Remove!=None:
            pass
        elif self.modes.Auto!=None:
            pass
        elif self.modes.URL!=[]:
            pass
        elif self.modes.Layout!=[]:
            pass

