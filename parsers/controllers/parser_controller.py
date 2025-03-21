import json
import asyncio
import logging
import itertools
from dataclasses import asdict
from fetchers.fetcher import Fetcher
from models.flyer_data import FlyerData
from parsers.main_page_parser import MainPageParser
from parsers.detail_page_parser import DetailPageParser


class ParserController:
    def __init__(
            self, 
            base_url: str="https://www.prospektmaschine.de/", 
            category: str="hypermarkte/", 
            fetcher_timeout: int=10, 
            verbose=False, 
            logger: logging.Logger=None):
        """
        Controller class for managing the parsing process of main and detail pages.

        This class is responsible for fetching HTML data from the main page and detail pages, 
        parsing the content using dedicated parsers, and saving the processed data to a file.

        Attributes:
            base_url (str): The base URL for the website to scrape.
            category (str): The category of items to scrape.
            fetcher_timeout (int): Timeout for fetching data.
            verbose (bool): Flag to enable verbose logging.
            logger (logging.Logger): Logger instance for logging events.
            main_page_parser (MainPageParser): Parser for the main page.
            detail_page_parsers (list): List of detail page parsers.
            fetcher (Fetcher): Fetcher instance for making HTTP requests.
            processed_data (list): List of processed data after parsing detail pages.

        Methods:
            process(): Asynchronously fetches and parses the main and detail pages.
            save_output(output_path): Saves the processed data to a JSON file.
        """
        self.logger = logger
        self.verbose = verbose 
        self.base_url = base_url
        self.category = category
        self.main_page_parser = MainPageParser(base_url, logger=logger)
        self.detail_page_parsers = []
        self.fetcher = Fetcher(fetcher_timeout, logger=logger)
        self.processed_data = []

    async def process(self) -> list[list[FlyerData]]:
        """
        Asynchronously fetches the main page and detail pages, parses them, 
        and returns the processed data.

        Fetches the main page, extracts links to detail pages, fetches the 
        detail pages, and parses them using individual detail page parsers.

        Returns:
            list: A list of list of processed data after parsing the detail pages. Or empty list if processing fails.
        """
        main_page_html = await self.fetcher.fetch(self.base_url + self.category)
        links = self.main_page_parser.parse(main_page_html)
        if not links: 
            self.logger.warning("No links found on the main page!")
            return [] 
        detail_pages = await self.fetcher.fetch_many(*links.values())
        detail_page_parsers = [DetailPageParser(shop_name) for shop_name in links.keys()]
        parser_tasks = [
            parser.async_parse(detail_page_html) 
            for parser, detail_page_html in zip(detail_page_parsers, detail_pages.values())
        ]
        data = await asyncio.gather(*parser_tasks)
        self.processed_data = data 
        return data

    def save_output(self, output_path):
        """
        Saves the processed data to a JSON file at the specified output path.

        Args:
            output_path (str): The path where the output file will be saved.
        """
        with open(output_path, "w", encoding="UTF-8") as output_file: 
            data = list(itertools.chain(*self.processed_data))
            output_file.write(json.dumps([asdict(d) for d in data]))
        if self.verbose:    
            self.logger.info(f"Scraping completed! Data saved to {output_path}")
        