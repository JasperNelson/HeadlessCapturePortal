#Debug backend for testing purposes
from Captr.backend import backend
from Captr.ConfigParser import Config
from Captr.LoginParser import Action, LoginParser
from typing import NamedTuple
class DebugBackend(backend):
    
    def URL_Fetch(self, URL: str, config: NamedTuple) -> str:
        print(f"URL:{URL}"+f"\n config:{config}")
        return "Debug"
    def Layout_Fetch(self, URL: str) -> str:
        print(f"URL:{URL}")
        return "Debug"
    def Move(self, locator: dict) -> bool:
        print(f"Move action -> locator:{locator}")
        return True
    def Text(self, locator: dict, value: str) -> bool:
        print(f"Text insert action -> locator:{locator}"+
              f"\n->value:{value}")
        return True
    def Wait(self, Timespan: int) -> bool:
        print(f"Waited {Timespan}")
        return True
    def Click(self, locator: dict) -> bool:
        print(f"clicked the object located at{locator}")
        return True