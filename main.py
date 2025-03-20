import os
import asyncio
import argparse
import nest_asyncio
from parsers.controllers.parser_controller import ParserController

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "data")

async def main():
    # CLI interface 
    parser = argparse.ArgumentParser(description="Scrape flyers from prospektmaschine.de")
    parser.add_argument(
        "--category",
        type=str,
        default="hypermarkte",
        help="Specify the category to scrape (default: hypermarkte)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join(data_dir, "output.json"),
        help="Specify the output JSON file path",
    )
    parser.add_argument(
        "--base_url", 
        type=str, 
        default="https://www.prospektmaschine.de/",
        help="Specify base url to be prepended to urls (default: 'https://www.prospektmaschine.de/')"
    )
    parser.add_argument(
        "--fetcher_timeout", 
        type=int, 
        default=10,
        help="Specify timeout for Fetcher class (default: 10)"
    )
    parser.add_argument(
        "--verbose", 
        type=bool, 
        default=False,
        help="Verbosity (default: False)"
    )

    args = parser.parse_args()
    args.category += "/" if args.category[-1] != "/" else ""
    args.base_url += "/" if args.base_url[-1] != "/" else ""
    
    parser_controller = ParserController(
        base_url=args.base_url,
        category=args.category, 
        fetcher_timeout=args.fetcher_timeout,
        verbose=args.verbose
    )

    # allow nested event loops

    nest_asyncio.apply()
    await parser_controller.process()
    parser_controller.save_output(args.output)


if __name__ == "__main__":
    asyncio.run(main())