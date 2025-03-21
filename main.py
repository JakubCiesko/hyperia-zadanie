import os
import logging
import asyncio
import argparse
from parsers.controllers.parser_controller import ParserController

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "data")

async def main():
    """
    Main entry point for the flyer scraping application.

    This function sets up the command-line interface (CLI) using argparse to accept 
    user inputs for category, output file path, base URL, fetcher timeout, verbosity, 
    and log file. It configures logging settings, initializes the `ParserController` 
    for fetching and parsing data, and saves the processed output to a specified 
    file in JSON format.

    The flow of the function is as follows:
        1. Parse command-line arguments.
        2. Configure logging based on verbosity and log file options.
        3. Initialize the `ParserController` with provided settings.
        4. Call `ParserController.process()` to fetch and parse data.
        5. Save the parsed data using `ParserController.save_output()`.

    Command-line arguments:
        --category (str): The category to scrape (default is "hypermarkte").
        --output (str): The output file path for saving the parsed data (default is 'data/output.json').
        --base_url (str): The base URL to scrape from (default is 'https://www.prospektmaschine.de/').
        --fetcher_timeout (int): Timeout for fetcher requests (default is 10).
        --verbose (bool): Flag to enable verbose logging (default is False).
        --log_file (str): Path to the log file (default is None, meaning logs are printed to the console).
    """

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
        action="store_true",
        help="Verbosity (default: False)",
    )
    parser.add_argument(
        "--log_file",
        type=str, 
        default=None,
        help="Specify log file path for logs to be saved (default: None - logs printed in CLI)"
    )

    args = parser.parse_args()
    args.category += "/" if args.category[-1] != "/" else ""
    args.base_url += "/" if args.base_url[-1] != "/" else ""

    # Logging settings 
    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(
        filename=args.log_file,
        level=level, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("fetchers.fetcher").setLevel(logging.INFO if args.verbose else logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.INFO if args.verbose else logging.WARNING)
    logger = logging.getLogger(__name__)

    # Main Logic: ParserController (Fetching + Parsing)
    parser_controller = ParserController(
        base_url=args.base_url,
        category=args.category, 
        fetcher_timeout=args.fetcher_timeout,
        logger=logger
    )

    _ = await parser_controller.process()
    parser_controller.save_output(args.output)


if __name__ == "__main__":
    asyncio.run(main())