from .page_scraper import PageScraper
from selectolax.parser import HTMLParser


class MainPageScraper(PageScraper):
    def __init__(self, base_url:str=""):
        self.base_url = base_url 

    def __call__(self, html_string: str) -> dict[str, str]:
        return self.parse(html_string)

    def parse(self, html_string:str) -> dict[str, str]:
        tree = HTMLParser(html_string)
        side_bar = tree.css_first("#sidebar")
        link_nodes = side_bar.css("li a")
        return {node.text(strip=True): self.base_url + node.attributes["href"] for node in link_nodes}