from .page_parser import PageParser
from models.flyer_data import FlyerData
from selectolax.parser import HTMLParser
from extractors.extractor import FlyerDataExtractor


class DetailPageParser(PageParser):
    def __init__(self, shop_name: str="", data_extractor: FlyerDataExtractor = None):
        self._shop_name = shop_name 
        self._extractor = data_extractor or FlyerDataExtractor()

    def set_shop_name(self, shop_name:str):
        self._shop_name = shop_name

    def get_shop_name(self) -> str: 
        return self._shop_name
    
    def set_data_extractor(self, data_extractor: FlyerDataExtractor):
        self._extractor = data_extractor
    
    def get_data_extractor(self) -> FlyerDataExtractor:
        return self._extractor

    def __call__(self, html_string:str) -> list[FlyerData]:
        return self.parse(html_string)

    def parse(self, html_string:str) -> list[FlyerData]:
        tree = HTMLParser(html_string)
        grid_with_fliers = tree.css_first(".letaky-grid")
        fliers = grid_with_fliers.css(".brochure-thumb")
        flier_data_extractor = self.get_data_extractor()
        return flier_data_extractor.extract(fliers, shop_name=self.get_shop_name())

    async def async_parse(self, html_string: str):
        tree = HTMLParser(html_string)
        grid_with_fliers = tree.css_first(".letaky-grid")
        fliers = grid_with_fliers.css(".brochure-thumb")
        flier_data_extractor = self.get_data_extractor()
        return flier_data_extractor.extract(fliers, shop_name=self.get_shop_name())