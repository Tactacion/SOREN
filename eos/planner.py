import anthropic
import settings as cfg
from models import Video, Scene
from typing import List
import json
import re

class VideoPlanner:
    """Create 3Blue1Brown style narrative"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=cfg.ANTHROPIC_KEY)
    
    def plan_videos(self, analysis: dict) -> List[Video]:
        """Create story-driven video plan"""
        
        print("  📋 Planning story arc...", end="", flush=True)
        
        prompt = f"""Create a 3Blue1Brown style video script.

<paper_analysis>
Title: {analysis['title']}
Hook: {analysis['hook']}
Problem: {analysis['problem']}
Key Insight: {analysis['key_insight']}
Why Clever: {analysis['why_clever']}

Concepts:
{json.dumps(analysis['concepts'], indent=2)}
</paper_analysis>

Your goal: Write a script that BUILDS INTUITION like Grant Sanderson.

═══════════════════════════════════════════════════════════
3BLUE1BROWN NARRATION STYLE
═══════════════════════════════════════════════════════════
- Conversational, not academic
- Questions to build curiosity
- "Let's think about..." instead of "We define..."
- Pauses for emphasis
- Casual language with precise concepts

═══════════════════════════════════════════════════════════
SCENE STRUCTURE (12 scenes total)
═══════════════════════════════════════════════════════════
Scene 1: HOOK - Start with puzzle/paradox
Scene 2-3: PROBLEM - Show what's broken
Scene 4-6: BUILD - Develop intuition step-by-step
Scene 7-9: INSIGHT - Reveal the key idea
Scene 10-11: POWER - Show what this enables
Scene 12: ZOOM OUT - Connect to bigger picture

═══════════════════════════════════════════════════════════
FOR EACH SCENE (THE "BEAT" SYSTEM)
═══════════════════════════════════════════════════════════

**THIS IS THE MOST IMPORTANT RULE.**

Do NOT write one big narration block.
You MUST break each scene into 5-10 small "Beats".
Each **Beat** is a single, short narration phrase (10-20 words) paired with a single, specific visual command.

Write:
1. **Title**: Simple, engaging (not technical)
2. **Purpose**: What "click" does this create?
3. **beats**: An array of 5-10 beat objects. Each beat object contains:
   * `narration_chunk`: A 10-20 word phrase.
   * `visual_command`: A *specific* Manim command for that single phrase.

═══════════════════════════════════════════════════════════
EXAMPLE SCENE (USING THE "BEAT" SYSTEM)
═══════════════════════════════════════════════════════════

{{
  "id": 1,
  "title": "The Three-Way Puzzle",
  "purpose": "Hook viewer with concrete visual puzzle",
  "beats": [
    {{
      "narration_chunk": "Imagine you have three probability distributions",
      "visual_command": "Create three particle clouds: 500 blue dots at LEFT*3, 500 green dots at ORIGIN, 500 orange dots at RIGHT*3"
    }},
    {{
      "narration_chunk": "The blue cloud represents input images",
      "visual_command": "Animate Text('Images', color=BLUE) appearing below the blue cloud"
    }},
    {{
      "narration_chunk": "The green cloud represents text descriptions",
      "visual_command": "Animate Text('Text', color=GREEN) appearing below the green cloud"
    }},
    {{
      "narration_chunk": "And the orange cloud represents output images",
      "visual_command": "Animate Text('Outputs', color=ORANGE) appearing below the orange cloud"
    }},
    {{
      "narration_chunk": "How do you connect all three simultaneously?",
      "visual_command": "Show three question marks appearing between the clouds"
    }}
  ]
}}

═══════════════════════════════════════════════════════════
NOW CREATE THE SCRIPT
═══════════════════════════════════════════════════════════

Create 12 scenes broken into 5-10 beats EACH.
Return JSON:
{{
  "video": {{
    "number": 1,
    "title": "Engaging title",
    "scenes": [...]
  }}
}}
`````json
"""

        response = self.client.messages.create(
            model=cfg.MODEL,
            max_tokens=16384,
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}]
        )
        
        print(" ✅")
        
        content = response.content[0].text
        match = re.search(r'```(?:json)?\n(.*?)\n```', content, re.DOTALL)
        data = json.loads(match.group(1) if match else content)
        
        video_data = data['video']
        scenes = []
        
        for s in video_data['scenes']:
            if 'beats' not in s or not s['beats']:
                continue

            full_narration = " ".join([beat['narration_chunk'] for beat in s['beats']])
            
            full_visuals = "\n\n".join([
                f"# Narration: \"{beat['narration_chunk']}\"\n# Visual: {beat['visual_command']}"
                for beat in s['beats']
            ])
            
            scenes.append(Scene(
                id=s['id'],
                title=s['title'],
                narration=full_narration,
                visual_instructions=full_visuals,
                cleanup_previous=True
            ))
        
        return [Video(
            number=video_data['number'],
            title=video_data['title'],
            theme='tech',
            scenes=scenes
        )]
    





