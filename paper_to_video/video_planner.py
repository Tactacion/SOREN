import anthropic
import json
from typing import List, Dict
from generators.models import Video, Scene, ScreenState
import config

class VideoPlanner:
    """Plans coherent video series from paper"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_KEY)
    
    def plan_video_series(self, paper_text: str) -> List[Video]:
        """Plan 4-5 coherent videos from paper"""
        
        prompt = f"""Analyze this ML paper and create a 4-video series plan.

Paper (first 8000 chars):
{paper_text[:8000]}

Create exactly 4 videos:
1. "The Problem" - What problem does this solve? Why does it matter?
2. "Core Innovation" - What's the key insight/method?
3. "How It Works" - Technical details, architecture
4. "Results & Impact" - Performance, applications, future

For each video, provide:
- Title
- Theme (one word)
- 8 scenes (30 seconds each = 4 minutes total)
- Each scene needs: title, narration (2-3 sentences), visual elements

Return as JSON:
{{
    "videos": [
        {{
            "number": 1,
            "title": "The Problem",
            "theme": "problem",
            "scenes": [
                {{
                    "id": 1,
                    "title": "Scene Title",
                    "narration": "2-3 sentences",
                    "duration": 30,
                    "visual_instructions": ["element1", "element2"]
                }}
            ]
        }}
    ]
}}
"""
        
        response = self.client.messages.create(
            model=config.MODEL,
            max_tokens=6000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        data = self._extract_json(response.content[0].text)
        
        videos = []
        for v in data['videos']:
            scenes = []
            for s in v['scenes']:
                scenes.append(Scene(
                    id=s['id'],
                    title=s['title'],
                    narration=s['narration'],
                    duration=s['duration'],
                    visual_instructions=s['visual_instructions'],
                    screen_state=ScreenState()
                ))
            
            videos.append(Video(
                number=v['number'],
                title=v['title'],
                theme=v['theme'],
                scenes=scenes,
                total_duration=sum(s.duration for s in scenes)
            ))
        
        return videos
    
    def _extract_json(self, text: str) -> dict:
        """Extract JSON from response"""
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Fallback
        return {
            "videos": [{
                "number": 1,
                "title": "Overview",
                "theme": "introduction",
                "scenes": [{
                    "id": 1,
                    "title": "Introduction",
                    "narration": "Let's explore this paper.",
                    "duration": 30,
                    "visual_instructions": ["Title card"]
                }]
            }]
        }