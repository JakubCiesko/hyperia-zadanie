from .page_parser import PageParser
from selectolax.parser import HTMLParser


class MainPageParser(PageParser):
    def __init__(self, base_url:str=""):
        self._base_url = base_url 

    def set_base_url(self, base_url:str):
        self._base_url = base_url
    
    def get_base_url(self) -> str: 
        return self._base_url

    def __call__(self, html_string: str) -> dict[str, str]:
        return self.parse(html_string)

    def parse(self, html_string:str) -> dict[str, str]:
        tree = HTMLParser(html_string)
        side_bar = tree.css_first("#sidebar")
        link_nodes = side_bar.css("li a")
        return {
            node.text(strip=True): self.get_base_url() + node.attributes.get("href") 
            for node in link_nodes
        }