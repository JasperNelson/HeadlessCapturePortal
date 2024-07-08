#Houses all of the portions of the backend that need to be implemented
from abc import ABC, abstractmethod
from Captr.ConfigParser import Config
from Captr.LoginParser import LoginParser
from typing import NamedTuple
class backend(ABC):
    @abstractmethod
    def URL_Fetch(self, URL: str, config: NamedTuple) -> str:
        pass
    @abstractmethod
    def Layout_Fetch(self, URL: str) -> str:
        pass
    @abstractmethod
    def Move(self, locator: dict) -> bool:
        pass
    @abstractmethod
    def Text(self, locator: dict, value: str) -> bool:
        pass
    @abstractmethod
    def Wait(self, Timespan: int) -> bool:
        pass
    @abstractmethod
    def Click(self, locator: dict) -> bool:
        pass


