#backend that simply uses the information from the config as well as argparse and implements it. 
from Captr.backend import backend
from Captr.ConfigParser import Config
from Captr.LoginParser import Action, LoginParser
from typing import NamedTuple
#NOTE: right now this is simply a copy of DebugBackend! the real simplebackend will be implemented later. 
class SimpleBackend(backend):
    
    def URL_Fetch(self, URL: str, config: NamedTuple) -> str:
        print(f"URL:{URL}"+f"\n config:{config}")
        return "simple"
    def Layout_Fetch(self, URL: str) -> str:
        print(f"URL:{URL}")
        return "simple"
    def Start(self, URLstart: str | None ) -> bool: #default url if given
        print(f"Move action -> URLstart:{URLstart}")
        return True
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