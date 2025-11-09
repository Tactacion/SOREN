from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json

@dataclass
class ScreenState:
    """Tracks what's currently on screen"""
    objects: List[str] = field(default_factory=list)
    occupied_zones: List[str] = field(default_factory=list)
    last_animation_type: str = ""
    
    def to_dict(self):
        return {
            'objects': self.objects,
            'occupied_zones': self.occupied_zones,
            'last_animation_type': self.last_animation_type
        }
    
    def add_object(self, obj_name: str, zone: str):
        self.objects.append(obj_name)
        if zone not in self.occupied_zones:
            self.occupied_zones.append(zone)
    
    def remove_object(self, obj_name: str):
        if obj_name in self.objects:
            self.objects.remove(obj_name)
    
    def clear_zone(self, zone: str):
        if zone in self.occupied_zones:
            self.occupied_zones.remove(zone)
    
    def clear_all(self):
        self.objects = []
        self.occupied_zones = []

@dataclass
class Scene:
    id: int
    title: str
    narration: str
    duration: float
    visual_instructions: List[str]
    screen_state: ScreenState = field(default_factory=ScreenState)

@dataclass
class Video:
    number: int
    title: str
    theme: str
    scenes: List[Scene]
    total_duration: float