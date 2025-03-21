import logging
from .page_parser import PageParser
from selectolax.parser import HTMLParser

class MainPageParser(PageParser):
    """
    A parser for extracting category links from the main page.

    This class is responsible for parsing the main page of a website
    and extracting category URLs from the sidebar navigation.

    Attributes:
        _base_url (str): The base URL of the website.
        logger (logging.Logger, optional): Logger for error handling and debugging.

    Methods:
        set_base_url(base_url: str):
            Sets the base URL for constructing full links.

        get_base_url() -> str:
            Retrieves the base URL.

        __call__(html_string: str) -> dict[str, str]:
            Calls the `parse` method, allowing the parser to be used as a function.

        parse(html_string: str) -> dict[str, str]:
            Parses the main page HTML and extracts category links.
    """

    def __init__(self, base_url:str = "", logger: logging.Logger = None):
        """
        Initializes the MainPageParser with an optional base URL and logger.

        Args:
            base_url (str, optional): The base URL of the website. Defaults to an empty string.
            logger (logging.Logger, optional): Logger instance for error handling. Defaults to None.
        """

        self._base_url = base_url 
        self.logger = logger 

    def set_base_url(self, base_url:str):
        """
        Sets the base URL of the website.

        Args:
            base_url (str): The base URL to be used for constructing full category links.
        """
        self._base_url = base_url
    
    def get_base_url(self) -> str: 
        """
        Retrieves the base URL of the website.

        Returns:
            str: The base URL.
        """
        return self._base_url

    def __call__(self, html_string: str) -> dict[str, str]:
        """
        Calls the `parse` method, making the parser instance callable.

        Args:
            html_string (str): The HTML content of the main page.

        Returns:
            dict[str, str]: A dictionary mapping category names to their URLs. Empty dict returned if error occurs.
        """
        return self.parse(html_string)

    def parse(self, html_string:str) -> dict[str, str]:
        """
        Parses the main page HTML and extracts category links.

        This method locates the sidebar, finds all category links, and
        constructs full URLs using the base URL.

        Args:
            html_string (str): The HTML content of the main page.

        Returns:
            dict[str, str]: A dictionary where keys are category names and values are their corresponding URLs. Empty dict returned if error occurs.

        Raises:
            Exception: Logs an error if parsing fails.
        """
        try: 
            tree = HTMLParser(html_string)
            side_bar = tree.css_first("#sidebar")
            link_nodes = side_bar.css("li a")
            return {
                node.text(strip=True): self.get_base_url() + node.attributes.get("href") 
                for node in link_nodes
            }
        except Exception as e: 
            self.logger.error(f"Error Parsing Main Page: {e}")
            return {}