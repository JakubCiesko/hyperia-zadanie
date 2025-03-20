import asyncio
from fetchers.fetcher import Fetcher
from parsers.main_page_parser import MainPageParser
from parsers.detail_page_parser import DetailPageParser


class ParserController:
    def __init__(self, base_url: str="https://www.prospektmaschine.de/", category: str="hypermarkte", fetcher_timeout: int=10, verbose=False):
        self.verbose = verbose 
        self.base_url = base_url
        self.category = category
        self.main_page_parser = MainPageParser(base_url)
        self.detail_page_parsers = []
        self.fetcher = Fetcher(fetcher_timeout) 

    def process(self):
        main_page_html = asyncio.run(self.fetcher.fetch(self.base_url + self.category))
        links = self.main_page_parser.parse(main_page_html)
        detail_pages = self.fetcher.fetch_many(*links.values())
        return detail_pages
        