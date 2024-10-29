# Houses all of the portions of the backend that need to be implemented
from abc import ABC, abstractmethod


class backend(ABC):

    @abstractmethod
    def Layout_Fetch(self, URL: str) -> str:
        pass

    @abstractmethod
    def Start(self, URLstart: str) -> bool:  # default url if given
        pass

    @abstractmethod
    def Move(self, locator: dict) -> bool:
        pass

    @abstractmethod
    def Text(self, locator: dict, value: str) -> bool:
        pass

    @abstractmethod
    def Wait(self, timespan: int) -> bool:
        pass

    @abstractmethod
    def Click(self, locator: dict) -> bool:
        pass
    
    @abstractmethod
    def PrintPage(self) -> str:
        pass