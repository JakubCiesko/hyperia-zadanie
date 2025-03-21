import json
from datetime import datetime
from dataclasses import dataclass, field, asdict

@dataclass
class FlyerData:
    """
    A data model representing a flyer, including its title, thumbnail, shop name, 
    validity period, and the time it was parsed.

    Attributes:
        title (str): The title of the flyer.
        thumbnail (str): The URL of the flyer's thumbnail image.
        shop_name (str): The name of the shop associated with the flyer.
        valid_from (str): The start date of the flyer's validity period (ISO 8601 format).
        valid_to (str): The end date of the flyer's validity period (ISO 8601 format).
        parsed_time (str): The timestamp when the flyer was parsed (default: current time in ISO format).
    """
    title: str
    thumbnail: str
    shop_name: str
    valid_from: str
    valid_to: str
    parsed_time: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_json(self) -> str:
        """
        Serializes the FlyerData instance into a JSON-formatted string.

        Returns:
            str: A JSON representation of the flyer data.
        """
        return json.dumps(asdict(self), indent=2)
