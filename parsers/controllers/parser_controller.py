import json
import logging
import asyncio
import itertools
from dataclasses import asdict
from fetchers.fetcher import Fetcher
from parsers.main_page_parser import MainPageParser
from parsers.detail_page_parser import DetailPageParser

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ParserController:
    def __init__(self, base_url: str="https://www.prospektmaschine.de/", category: str="hypermarkte/", fetcher_timeout: int=10, verbose=False):
        self.verbose = verbose 
        self.base_url = base_url
        self.category = category
        self.main_page_parser = MainPageParser(base_url)
        self.detail_page_parsers = []
        self.fetcher = Fetcher(fetcher_timeout)
        self.processed_data = []

    async def process(self):
        main_page_html = asyncio.run(self.fetcher.fetch(self.base_url + self.category))
        links = self.main_page_parser.parse(main_page_html)
        detail_pages = await self.fetcher.fetch_many(*links.values())
        detail_page_parsers = [DetailPageParser(shop_name) for shop_name in links.keys()]
        parser_tasks = [parser.async_parse(detail_page_html) for parser, detail_page_html in zip(detail_page_parsers, detail_pages.values())]
        data = await asyncio.gather(*parser_tasks)
        self.processed_data = data 
        return data

    def save_output(self, output_path):
        with open(output_path, "w", encoding="UTF-8") as output_file: 
            data = list(itertools.chain(*self.processed_data))
            output_file.write(json.dumps([asdict(d) for d in data]))
        if self.verbose:    
            logging.info(f"Scraping completed! Data saved to {output_path}")
        