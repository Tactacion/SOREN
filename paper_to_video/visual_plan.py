# visual_plan.py - NEW FILE

from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum

class ObjectType(Enum):
    CIRCLE = "Circle"
    SQUARE = "Square"
    RECTANGLE = "Rectangle"
    DOT = "Dot"
    TEXT = "Text"
    MATHTEX = "MathTex"
    ARROW = "Arrow"
    LINE = "Line"
    AXES = "Axes"
    VGROUP = "VGroup"

class AnimationType(Enum):
    CREATE = "Create"
    WRITE = "Write"
    FADEIN = "FadeIn"
    FADEOUT = "FadeOut"
    TRANSFORM = "Transform"
    LAGGEDSTART = "LaggedStart"
    INDICATE = "Indicate"
    CIRCUMSCRIBE = "Circumscribe"

@dataclass
class VisualObject:
    """Concrete visual object specification"""
    id: str
    type: ObjectType
    params: Dict[str, Any]
    position: List[float] = field(default_factory=lambda: [0, 0, 0])

@dataclass
class Animation:
    """Concrete animation specification"""
    type: AnimationType
    target: str  # Object ID or list of IDs
    duration: float
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Timeline:
    """Timeline of animations"""
    start_time: float
    animations: List[Animation]

@dataclass
class VisualPlan:
    """Complete executable visual plan for a scene"""
    objects: List[VisualObject]
    timelines: List[Timeline]
    total_duration: float
    
    def to_code(self) -> str:
        """Convert plan to Manim code"""
        code_lines = []
        
        # Create all objects
        for obj in self.objects:
            code_lines.append(self._object_to_code(obj))
        
        # Create animations in timeline order
        for timeline in sorted(self.timelines, key=lambda t: t.start_time):
            for anim in timeline.animations:
                code_lines.append(self._animation_to_code(anim))
        
        return '\n'.join(code_lines)
    
    def _object_to_code(self, obj: VisualObject) -> str:
        """Convert object to Manim code"""
        params_str = ', '.join([f"{k}={repr(v)}" for k, v in obj.params.items()])
        
        code = f"{obj.id} = {obj.type.value}({params_str})"
        
        if obj.position != [0, 0, 0]:
            code += f"\n{obj.id}.move_to({obj.position})"
        
        return code
    
    def _animation_to_code(self, anim: Animation) -> str:
        """Convert animation to Manim code"""
        params_str = ', '.join([f"{k}={repr(v)}" for k, v in anim.params.items()])
        
        if anim.type == AnimationType.LAGGEDSTART:
            # Special case for LaggedStart
            return f"self.play({anim.type.value}(*{anim.target}, {params_str}), run_time={anim.duration})"
        else:
            return f"self.play({anim.type.value}({anim.target}, {params_str}), run_time={anim.duration})"


class VisualPlanner:
    """Generate visual plans from scene descriptions"""
    
    def __init__(self, client):
        self.client = client
    
    def plan(self, scene_title: str, narration: str, visual_instructions: str) -> VisualPlan:
        """Generate executable visual plan"""
        
        prompt = f"""Create a CONCRETE visual plan for this scene.

SCENE: {scene_title}
NARRATION: {narration}
VISUAL: {visual_instructions}

Generate a JSON plan with:
1. Objects: List of visual objects with EXACT parameters
2. Timeline: Sequence of animations with EXACT timings

Example format:
{{
  "objects": [
    {{
      "id": "title",
      "type": "Text",
      "params": {{"text": "Title", "font_size": 42, "color": "WHITE"}},
      "position": [0, 3.2, 0]
    }},
    {{
      "id": "circle1",
      "type": "Circle",
      "params": {{"radius": 0.5, "color": "BLUE", "fill_opacity": 0.5}},
      "position": [-2, 0, 0]
    }}
  ],
  "timeline": [
    {{
      "start_time": 0,
      "animations": [
        {{
          "type": "Write",
          "target": "title",
          "duration": 2,
          "params": {{}}
        }}
      ]
    }},
    {{
      "start_time": 2,
      "animations": [
        {{
          "type": "FadeIn",
          "target": "circle1",
          "duration": 1.5,
          "params": {{"scale": 0.5}}
        }}
      ]
    }}
  ]
}}

Make it CONCRETE and EXECUTABLE.
"""

        response = self.client.messages.create(
            model=config.MODEL,
            max_tokens=6000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        json_match = re.search(r'\{.*\}', response.content[0].text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return self._parse_plan(data)
            except:
                pass
        
        # Fallback: return empty plan
        return VisualPlan(objects=[], timelines=[], total_duration=60)
    
    def _parse_plan(self, data: Dict) -> VisualPlan:
        """Parse JSON into VisualPlan"""
        objects = [
            VisualObject(
                id=obj['id'],
                type=ObjectType[obj['type'].upper()],
                params=obj['params'],
                position=obj.get('position', [0, 0, 0])
            )
            for obj in data.get('objects', [])
        ]
        
        timelines = [
            Timeline(
                start_time=t['start_time'],
                animations=[
                    Animation(
                        type=AnimationType[a['type'].upper()],
                        target=a['target'],
                        duration=a['duration'],
                        params=a.get('params', {})
                    )
                    for a in t['animations']
                ]
            )
            for t in data.get('timeline', [])
        ]
        
        total_duration = max([t.start_time + max([a.duration for a in t.animations], default=0) 
                             for t in timelines], default=60)
        
        return VisualPlan(objects=objects, timelines=timelines, total_duration=total_duration)