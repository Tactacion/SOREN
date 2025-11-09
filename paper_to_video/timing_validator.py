# timing_validator.py - ANIMATION TIMING VALIDATION

import re
from typing import Tuple

class TimingValidator:
    """Ensure animations match narration duration"""
    
    def validate(self, code: str, expected_duration: float) -> Tuple[bool, str, float]:
        """Check animation duration"""
        
        actual = self._calculate_duration(code)
        
        min_ok = expected_duration * 0.7
        max_ok = expected_duration * 1.3
        
        if actual < min_ok:
            return False, f"Too short: {actual:.1f}s (need ~{expected_duration:.0f}s)", actual
        elif actual > max_ok:
            return False, f"Too long: {actual:.1f}s (need ~{expected_duration:.0f}s)", actual
        else:
            return True, f"Good: {actual:.1f}s", actual
    
    def _calculate_duration(self, code: str) -> float:
        """Sum up all animation durations"""
        total = 0.0
        
        # self.play(..., run_time=X)
        for match in re.finditer(r'self\.play\([^)]*run_time\s*=\s*([0-9.]+)', code):
            total += float(match.group(1))
        
        # self.wait(X)
        for match in re.finditer(r'self\.wait\(([0-9.]+)\)', code):
            total += float(match.group(1))
        
        return total