from .page_parser import PageParser
from models.flyer_data import FlyerData
from selectolax.parser import HTMLParser
from extractors.extractor import FlyerDataExtractor


class DetailPageParser(PageParser):
    """
    A parser for extracting flyer data from a retailer's detail page.

    This class is responsible for parsing detail pages that contain
    flyer listings and extracting relevant information using the FlyerDataExtractor.

    Attributes:
        _shop_name (str): The name of the retailer.
        _extractor (FlyerDataExtractor): Extractor instance for processing flyer data.

    Methods:
        set_shop_name(shop_name: str):
            Sets the shop name for the parser.

        get_shop_name() -> str:
            Retrieves the shop name.

        set_data_extractor(data_extractor: FlyerDataExtractor):
            Sets the flyer data extractor instance.

        get_data_extractor() -> FlyerDataExtractor:
            Retrieves the flyer data extractor instance.

        __call__(html_string: str) -> list[FlyerData]:
            Calls the `parse` method, allowing the parser to be used as a function.

        parse(html_string: str) -> list[FlyerData]:
            Parses the detail page HTML and extracts flyer data.

        async_parse(html_string: str) -> list[FlyerData]:
            Asynchronous version of `parse` for handling flyer data extraction.
    """

    def __init__(self, shop_name: str="", data_extractor: FlyerDataExtractor = None):
        """
        Initializes the DetailPageParser with an optional shop name and data extractor.

        Args:
            shop_name (str, optional): The name of the shop. Defaults to an empty string.
            data_extractor (FlyerDataExtractor, optional): Extractor instance for flyer data. Defaults to None (Instantiaze FlyerDataExtractor class).
        """
        self._shop_name = shop_name 
        self._extractor = data_extractor or FlyerDataExtractor()

    def set_shop_name(self, shop_name:str):
        """
        Sets the shop name for the parser.

        Args:
            shop_name (str): The name of the shop.
        """
        self._shop_name = shop_name

    def get_shop_name(self) -> str: 
        """
        Retrieves the shop name.

        Returns:
            str: The name of the shop.
        """
        return self._shop_name
    
    def set_data_extractor(self, data_extractor: FlyerDataExtractor):
        """
        Sets the flyer data extractor instance.

        Args:
            data_extractor (FlyerDataExtractor): The extractor instance to process flyer data.
        """
        self._extractor = data_extractor
    
    def get_data_extractor(self) -> FlyerDataExtractor:
        """
        Retrieves the flyer data extractor instance.

        Returns:
            FlyerDataExtractor: The current flyer data extractor.
        """
        return self._extractor

    def __call__(self, html_string:str) -> list[FlyerData]:
        """
        Calls the `parse` method, making the parser instance callable.

        Args:
            html_string (str): The HTML content of the detail page.

        Returns:
            list[FlyerData]: A list of extracted flyer data.
        """
        return self.parse(html_string)

    def parse(self, html_string:str) -> list[FlyerData]:
        """
        Parses the detail page HTML and extracts flyer data.

        This method locates the flyer grid, extracts flyer elements,
        and uses the FlyerDataExtractor to process the information.

        Args:
            html_string (str): The HTML content of the detail page.

        Returns:
            list[FlyerData]: A list of flyer data objects.
        """
        tree = HTMLParser(html_string)
        grid_with_fliers = tree.css_first(".letaky-grid")
        fliers = grid_with_fliers.css(".brochure-thumb")
        flier_data_extractor = self.get_data_extractor()
        return flier_data_extractor.extract(fliers, shop_name=self.get_shop_name())

    async def async_parse(self, html_string: str):
        """
        Asynchronously parses the detail page HTML and extracts flyer data.

        This method works similarly to `parse`, but it can be used in
        an asynchronous workflow.

        Args:
            html_string (str): The HTML content of the detail page.

        Returns:
            list[FlyerData]: A list of flyer data objects.
        """
        tree = HTMLParser(html_string)
        grid_with_fliers = tree.css_first(".letaky-grid")
        fliers = grid_with_fliers.css(".brochure-thumb")
        flier_data_extractor = self.get_data_extractor()
        return flier_data_extractor.extract(fliers, shop_name=self.get_shop_name())