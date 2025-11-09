import anthropic
import settings as cfg
import json
import re

class PaperAnalyzer:
    """Extract insights and intuition, not just concepts"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=cfg.ANTHROPIC_KEY)
    
    def analyze(self, text: str) -> dict:
        """Extract the story of the paper"""
        
        print("  🔍 Analyzing paper...", end="", flush=True)
        
        prompt = f"""You are analyzing a research paper to create a 3Blue1Brown style educational video.

<paper_text>
{text[:40000]}
</paper_text>

Your goal: Extract the STORY and INTUITION, not just list concepts.

═══════════════════════════════════════════════════════════
WHAT 3BLUE1BROWN DOES DIFFERENTLY
═══════════════════════════════════════════════════════════
- Builds visual intuition progressively
- Uses analogies before formalism
- Shows WHY something works, not just HOW
- Creates "aha!" moments through visual discovery
- Connects abstract concepts to concrete visuals

═══════════════════════════════════════════════════════════
EXTRACT THESE ELEMENTS
═══════════════════════════════════════════════════════════

1. **Main Hook**: What surprising question does this paper answer?
2. **The Problem**: What's broken with current approaches? (2-3 sentences)
3. **Key Insight**: The ONE clever idea that changes everything (1 sentence)
4. **Why It's Clever**: Why this insight is brilliant (2-3 sentences)

═══════════════════════════════════════════════════════════
FOR EACH CONCEPT
═══════════════════════════════════════════════════════════

Extract 12 concepts that BUILD understanding:

For each concept provide:
- **Intuitive Title**: Not "f-divergence" but "Measuring How Different Two Distributions Are"
- **Hook**: One-sentence curiosity hook
- **Analogy**: Visual metaphor (e.g., "distributions are like clouds of particles")
- **Core Idea**: What you'd tell a smart friend
- **Why It Works**: The intuition behind the math
- **Visual Idea**: Give a 2-3 step visual *sequence* to demonstrate
- **Builds To**: What understanding this unlocks

═══════════════════════════════════════════════════════════
RETURN FORMAT
═══════════════════════════════════════════════════════════

Return a JSON with this structure:

{{
  "title": "Simple paper title for humans",
  "hook": "The intriguing question that starts the video",
  "problem": "What's broken with current approaches (2-3 sentences)",
  "key_insight": "The ONE clever idea (1 sentence)",
  "why_clever": "Why this insight is brilliant (2-3 sentences)",
  "concepts": [
    {{
      "id": 1,
      "title": "Intuitive title",
      "hook": "Curiosity hook",
      "analogy": "Visual metaphor",
      "core_idea": "What you'd tell a friend",
      "why_it_works": "The intuition",
      "visual_idea": "Specific 2-3 step visual sequence",
      "builds_to": "What this enables"
    }},
    ... (12 concepts total)
  ]
}}

Now analyze this paper with INTUITION and STORY focus.
``````json
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
        if match:
            return json.loads(match.group(1))
        return json.loads(content)