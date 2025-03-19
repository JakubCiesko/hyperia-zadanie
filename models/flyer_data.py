from datetime import datetime
from dataclasses import dataclass, field, asdict
import json

@dataclass
class FlyerData:
    title: str
    thumbnail: str
    shop_name: str
    valid_from: str
    valid_to: str
    parsed_time: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)
