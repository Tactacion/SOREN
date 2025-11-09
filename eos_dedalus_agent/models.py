# models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Scene:
    id: int
    title: str
    narration: str
    visual_instructions: str
    cleanup_previous: bool = True

@dataclass
class Video:
    number: int
    title: str
    theme: str
    scenes: List[Scene] = field(default_factory=list)
