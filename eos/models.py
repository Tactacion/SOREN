from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Concept:
    """A key concept from the paper"""
    id: str
    name: str
    intuition: str
    visual_idea: str
    prerequisites: List[str]

@dataclass
class VisualCommand:
    """Simple, safe visual instruction"""
    action: str  # CREATE, ANIMATE, TRANSFORM, etc.
    object_type: str  # Circle, Text, VGroup, etc.
    params: dict  # Safe parameters
    timing: float = 1.0

@dataclass
class VisualPlan:
    """Complete visual plan for a scene"""
    commands: List[VisualCommand]
    description: str

@dataclass
class Scene:
    """A single scene in a video"""
    id: int
    title: str
    narration: str
    visual_instructions: str
    cleanup_previous: bool = True

@dataclass
class Video:
    """A complete video with multiple scenes"""
    number: int
    title: str
    theme: str
    scenes: List[Scene]