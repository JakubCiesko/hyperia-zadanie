from abc import ABC, abstractmethod
from models.flyer_data import FlyerData

class PageParser(ABC):
    """
    An abstract base class for parsing web pages.

    This class defines a standard interface for parsing both main pages and detail pages.
    Implementing subclasses should define their own `parse` method.

    Methods:
        parse(html_string: str) -> dict[str, str] | list[FlyerData]:
            Parses the given HTML string and extracts relevant data.

        __call__(html_string: str) -> dict[str, str] | list[FlyerData]:
            A wrapper around `parse` to allow instances of the class to be callable.
    """
    @abstractmethod
    def parse(self, html_string:str) -> dict[str, str] | list[FlyerData]:
        """
        Parses the given HTML string.

        This method should be implemented by subclasses to extract relevant information 
        from the provided HTML content.

        Args:
            html_string (str): The HTML content to parse.

        Returns:
            dict[str, str] | list[FlyerData]: 
                A dictionary of extracted links (for main page parsers) 
                or a list of FlyerData objects (for detail page parsers).
        """
        pass 

    @abstractmethod
    def __call__(self, html_string: str) -> dict[str, str] | list[FlyerData]:
        """
        Calls the `parse` method, allowing the parser instance to be used like a function.

        Args:
            html_string (str): The HTML content to parse.

        Returns:
            dict[str, str] | list[FlyerData]: Parsed data from the given HTML content.
        """
        return self.parse(html_string) 