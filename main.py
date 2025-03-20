import os
import argparse
import logging
import asyncio
from fetchers.fetcher import Fetcher
from parsers.main_page_parser import MainPageParser
from parsers.detail_page_parser import DetailPageParser
from parsers.controllers.parser_controller import ParserController

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "data")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Scrape flyers from prospektmaschine.de")
    
    # CLI Arguments
    parser.add_argument(
        "--category",
        type=str,
        default="hypermarkte",
        help="Specify the category to scrape (default: hypermarkte)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join(data_dir,"data/output.json"),
        help="Specify the output JSON file path",
    )

    args = parser.parse_args()

    base_url = "https://www.prospektmaschine.de/"
    logging.info(f"Starting scraper for category: {args.category}")
    
    #fetcher = Fetcher()
    #main_page_parser = MainPageParser(base_url=base_url)
    
    #shop_links = asyncio.run(fetcher.fetch())
    ParserController(base_url)

    
    
    
    logging.info(f"Scraping completed! Data saved to {args.output}")


if __name__ == "__main__":
    main()