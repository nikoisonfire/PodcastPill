from dataclasses import dataclass
from typing import List

@dataclass
class Podcast:
    id: int
    title: str
    description: str
    image: str
    categories: List[str]
    weightedDrops: List[float]
