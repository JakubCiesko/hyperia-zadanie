from abc import ABC, abstractmethod

class PageScraper(ABC):

    @abstractmethod
    def parse(self, html_string:str) -> dict[str, str]:
        pass 

    @abstractmethod
    def __call__(self, html: str):
        pass 