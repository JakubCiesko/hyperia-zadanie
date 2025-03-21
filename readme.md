# Flyer Scraping Application

This Python script scrapes flyers from the website "https://www.prospektmaschine.de/" using different parsers for the main and detail pages. You can specify various parameters through the command-line interface (CLI) to customize the scraping behavior.

## Requirements

Mainly asyncio, argparse, httpx and selectolax. All specified in requirements.txt

## Usage

### Running the Script

To run the script, simply execute the following command:

```bash
python main.py
```

This is equivalent to 

```bash
python main.py --category "hypermarkte" --output "data/output.json" --base_url "https://www.prospektmaschine.de/" --fetcher_timeout 10
```

### Argument Explanation 

```--category "hypermarkte"```: Specifies the category to scrape, which is "hypermarkte" in this case.


```--output "data/output.json"```: Specifies the output file where the parsed data will be saved.


```--base_url "https://www.prospektmaschine.de/"```: Specifies the base URL to scrape from.


```--fetcher_timeout 10```: Sets the timeout for the fetcher to 10 seconds.


```--verbose```: Enables verbose logging, which will print more detailed logs to the console or logfile.


```--log_file```: Specifies path to logfile to print logs instead of printing them straight in CLI.