import anthropic
from pathlib import Path
from generators.models import Scene, Video, ScreenState
import config
import json

class ManimGenerator:
    """Generates Manim code with proper state management"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_KEY)
    
    def generate_video_code(self, video: Video, output_dir: Path):
        """Generate all scenes for a video"""
        
        current_state = ScreenState()
        
        for i, scene in enumerate(video.scenes):
            # Update state from previous scene
            scene.screen_state = current_state
            
            # Generate code
            code, new_state = self._generate_scene_with_state(scene, video.theme)
            
            # Save code
            scene_file = output_dir / f"video{video.number}_scene{scene.id}.py"
            scene_file.write_text(code)
            
            # Update state for next scene
            current_state = new_state
            
            print(f"  Generated: {scene_file.name}")
    
    def _generate_scene_with_state(self, scene: Scene, theme: str):
        """Generate scene code that respects screen state"""
        
        zones_json = json.dumps(config.ZONES)
        colors_json = json.dumps(config.COLORS)
        state_json = json.dumps(scene.screen_state.to_dict())
        
        prompt = f"""Generate Manim code for this scene.

SCENE: {scene.title}
NARRATION: {scene.narration}
VISUAL ELEMENTS: {', '.join(scene.visual_instructions)}
DURATION: {scene.duration} seconds
THEME: {theme}

CURRENT SCREEN STATE:
{state_json}

AVAILABLE ZONES (never place objects outside these):
{zones_json}

COLOR SCHEME:
{colors_json}

CRITICAL RULES:
1. FIRST: If objects on screen from previous scene, fade them out
2. Use only the defined ZONES for positioning
3. Never let objects go off screen (stay within x:[-6,6], y:[-3.5,3.5])
4. Track what you add to screen
5. Clean up before adding new elements to same zone
6. Use consistent colors based on theme

Generate:
1. Complete Scene class code (no imports)
2. List of objects that will be on screen at END of scene

Return format:
```python
[scene code here]
```

FINAL_STATE: [list of objects remaining on screen]
"""
        
        response = self.client.messages.create(
            model=config.MODEL,
            max_tokens=5000,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.content[0].text
        
        # Extract code
        code = self._extract_code(text)
        wrapped_code = self._wrap_code(code, scene.id, video.number, scene.narration)
        
        # Extract new state
        new_state = self._extract_state(text)
        
        return wrapped_code, new_state
    
    def _extract_code(self, text: str) -> str:
        """Extract code from response"""
        import re
        code_match = re.search(r'```python\n(.*?)\n```', text, re.DOTALL)
        if code_match:
            return code_match.group(1)
        
        # Fallback - return everything that looks like code
        lines = text.split('\n')
        code_lines = [l for l in lines if not l.startswith('FINAL_STATE')]
        return '\n'.join(code_lines)
    
    def _extract_state(self, text: str) -> ScreenState:
        """Extract final screen state"""
        import re
        state_match = re.search(r'FINAL_STATE:\s*\[(.*?)\]', text)
        
        new_state = ScreenState()
        if state_match:
            objects = state_match.group(1).split(',')
            new_state.objects = [o.strip().strip('"\'') for o in objects if o.strip()]
        
        return new_state
    
    def _wrap_code(self, code: str, scene_id: int, video_num: int, narration: str) -> str:
        """Wrap code with imports and voice setup"""
        
        # Clean narration for Python string
        clean_narration = narration.replace('"', '\\"')
        
        template = f'''from manim import *
import numpy as np
import os

# Zone definitions
ZONES = {{
    'title': np.array([0, 3.2, 0]),
    'top_left': np.array([-4, 2, 0]),
    'top_right': np.array([4, 2, 0]),
    'left': np.array([-4, 0, 0]),
    'center': np.array([0, 0, 0]),
    'right': np.array([4, 0, 0]),
    'bottom_left': np.array([-4, -2, 0]),
    'bottom_right': np.array([4, -2, 0]),
    'bottom': np.array([0, -2.5, 0])
}}

# Colors
BLUE = "#58C4DD"
GREEN = "#8BE17D"
ORANGE = "#FFB74D"
RED = "#FF6188"
WHITE = "#FFFFFF"

class Video{video_num}Scene{scene_id}(Scene):
    def construct(self):
        # Narration: "{clean_narration}"
        
{self._indent_code(code)}
'''
        return template
    
    def _indent_code(self, code: str) -> str:
        """Indent code for class method"""
        lines = code.split('\n')
        return '\n'.join('        ' + line if line.strip() else '' for line in lines)