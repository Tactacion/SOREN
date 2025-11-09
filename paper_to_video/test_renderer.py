# test_renderer.py - NEW FILE

import subprocess
import tempfile
from pathlib import Path
from typing import Tuple

class TestRenderer:
    """Validate code by test rendering"""
    
    def validate_scene(self, scene_code: str) -> Tuple[bool, str]:
        """Test render a scene to check for crashes"""
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            test_code = self._wrap_for_test(scene_code)
            f.write(test_code)
            temp_file = Path(f.name)
        
        try:
            # Run manim in dry-run mode (no actual rendering)
            result = subprocess.run(
                ['python', '-m', 'manim', '--dry_run', str(temp_file), 'TestScene'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "Test render successful"
            else:
                error_msg = result.stderr[-500:]  # Last 500 chars
                return False, f"Test render failed: {error_msg}"
        
        except subprocess.TimeoutExpired:
            return False, "Test render timeout"
        except Exception as e:
            return False, f"Test render error: {str(e)}"
        finally:
            # Cleanup
            temp_file.unlink(missing_ok=True)
    
    def _wrap_for_test(self, scene_code: str) -> str:
        """Wrap scene code in minimal test class"""
        return f'''from manim import *
import numpy as np

ZONES = {{
    'title': np.array([0, 3.2, 0]),
    'center': np.array([0, 0, 0]),
    'left': np.array([-4, 0, 0]),
    'right': np.array([4, 0, 0]),
    'top_left': np.array([-4, 2, 0]),
    'top_right': np.array([4, 2, 0]),
    'bottom': np.array([0, -2.5, 0])
}}

BLUE = "#58C4DD"
GREEN = "#8BE17D"
ORANGE = "#FFB74D"
RED = "#FF6188"
YELLOW = "#FFD700"
GOLD = "#FFD700"
PURPLE = "#C678DD"
GRAY = "#888888"
WHITE = "#FFFFFF"
BLACK = "#000000"

class TestScene(Scene):
    def construct(self):
{self._indent(scene_code, 8)}
'''
    
    def _indent(self, code: str, spaces: int) -> str:
        """Indent code block"""
        indent = ' ' * spaces
        return '\n'.join([indent + line if line.strip() else line 
                          for line in code.split('\n')])