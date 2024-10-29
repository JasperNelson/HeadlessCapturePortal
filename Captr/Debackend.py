#Debug backend for testing purposes
from Captr.backend import backend


class DebugBackend(backend):
    def Layout_Fetch(self, URL: str) -> str:
        print(f"This is layout_fetch we recieved the :{URL}")
        return "simple"
    def Start(self, URLstart: str | None) -> bool:  #default url if given
        print(f"Starting process -> URLstart:{URLstart}")
        return True
    def Move(self, locator: dict) -> bool:
        print(f"Move action -> locator:{locator}")
        return True
    def Text(self, locator: dict, value: str) -> bool:
        print(f"Text insert action -> locator:{locator}" + f"\n->value:{value}")
        return True
    def Wait(self, Timespan: int) -> bool:
        print(f"Waited {Timespan}")
        return True
    def Click(self, locator: dict) -> bool:
        print(f"clicked the object located at{locator}")
        return True
    def PrintPage(self) -> str:
        print(f"prints page")
        return "Foo"
        
