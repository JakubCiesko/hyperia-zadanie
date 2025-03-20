from models.flyer_data import FlyerData
from selectolax.parser import Node
from datetime import datetime

class FlyerDataExtractor:
    def __init__(self):
        pass

    def extract(self, fliers: list[Node], shop_name: str) -> list[FlyerData]:
        if isinstance(fliers, Node):
            fliers = [fliers]
        return [self._extract_flyer_info(flyer, shop_name) for flyer in fliers]

    def _extract_flyer_info(self, flyer: Node, shop_name:str) -> FlyerData:
        flyer_contents = flyer.css_first(".letak-description").css(".grid-item-content") 
        if flyer_contents:
            thumbnail_node = flyer.css_first("picture img")
            flyer_thumbnail = self._get_thumbnail_src(thumbnail_node) # need to fetch better image quality by clicking the <a> tag...
            from_to_date = flyer_contents[1].css_first(".visible-sm").text(strip=True)
            valid_from, valid_to = self._parse_dates(from_to_date)
            title = flyer_contents[0].text(strip=True)
        else: 
            flyer_thumbnail, valid_from, valid_to, title = "", "", "", ""

        return FlyerData(
            title=title,
            thumbnail=flyer_thumbnail,
            shop_name=shop_name,
            valid_from=valid_from,
            valid_to=valid_to
        )

    def _parse_dates(self, dates: list[str]) -> tuple[str, str]:
        dates = dates.split("-")
        if len(dates) >= 2:
            start_date_raw, end_date_raw = dates[0].strip(), dates[1].strip()
            end_date = datetime.strptime(end_date_raw, "%d.%m.%Y")
            start_date = datetime.strptime(
                f"{start_date_raw}{end_date.year}", "%d.%m.%Y"
            )
            return start_date.isoformat(), end_date.isoformat()
        return dates[0].strip(), ""
    
    def _get_thumbnail_src(self, thumbnail_node: Node) -> str:
        thumbnail_src = thumbnail_node.attributes.get("src") # need to account for thumbnails of better quality
        thumbnail_data_src = thumbnail_node.attributes.get("data-src")
        src = thumbnail_src or thumbnail_data_src
        return src or ""

    def _polish_thumbnail_src(self, src: str) -> str: 
        if src:
            jpg_extension_index = src.find(".jpg")
            src = src[:jpg_extension_index] if jpg_extension_index >= 0 else src 
            return src
        return ""