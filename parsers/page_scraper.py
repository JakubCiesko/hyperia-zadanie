from abc import ABC, abstractmethod
from models.flyer_data import FlyerData

class PageParser(ABC):
    @abstractmethod
    def parse(self, html_string:str) -> dict[str, str] | list[FlyerData]:
        pass 

    @abstractmethod
    def __call__(self, html_string: str) -> dict[str, str] | list[FlyerData]:
        return self.parse(html_string) 