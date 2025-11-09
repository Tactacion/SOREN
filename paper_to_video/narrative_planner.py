# narrative_planner.py
import anthropic
import config
import json
import re
from typing import Dict

class NarrativePlanner:
    """Plans video narrative structure with a story arc"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_KEY)

    def plan_narrative_from_dict(self, paper_data: Dict) -> Dict:
        """Plan narrative from paper dictionary (for compatibility)"""

        prompt = f"""
Analyze this research paper and extract its narrative structure.
PAPER TITLE: {paper_data.get('title', 'Unknown')}
ABSTRACT: {paper_data.get('abstract', '')}
CONTENT SAMPLE: {paper_data.get('content', '')[:2000]}

Return JSON with narrative beats for an 8-scene video:
```json
{{
  "hook": {{
    "title": "Scene 1: The Problem",
    "problem": "What is the core problem?",
    "why_care": "Why is this problem hard/important?",
    "visual_idea": "A dramatic visualization of the problem"
  }},
  "context": {{
    "title": "Scene 2: Previous Attempts",
    "previous_attempts": "What have others tried?",
    "limitations": "Why did those attempts fail or fall short?",
    "visual_idea": "Show 2-3 previous methods and their flaws"
  }},
  "insight": {{
    "title": "Scene 3: The Key Insight",
    "aha_moment": "What is the paper's core innovation?",
    "why_clever": "Why is this a smart solution?",
    "visual_idea": "A clear 'aha' moment visualization"
  }},
  "mechanism": [
    {{
      "title": "Scene 4: How It Works (Part 1)",
      "explanation": "The high-level overview of the method",
      "visual_idea": "A system diagram or high-level flow"
    }},
    {{
      "title": "Scene 5: How It Works (Part 2)",
      "explanation": "The most important technical detail or math",
      "visual_idea": "A focused visualization of the math/logic"
    }}
  ],
  "validation": {{
    "title": "Scene 6: The Results",
    "key_result": "What is the most impressive experimental result?",
    "comparison": "How does it compare to baselines?",
    "visual_idea": "A clear bar chart or graph showing the win"
  }},
  "implications": {{
    "title": "Scene 7: Why This Matters",
    "unlocks": "What new things does this enable?",
    "broader_impact": "What is the broader impact on the field?",
    "visual_idea": "Visualization of new applications"
  }},
  "conclusion": {{
    "title": "Scene 8: The Future",
    "future_work": "What are the next steps or open questions?",
    "callback": "A final summary that callbacks to the Scene 1 problem",
    "visual_idea": "A concluding visual looking forward"
  }},
  "theme": {{
    "main_concept_color": "BLUE",
    "comparison_color": "ORANGE",
    "result_color": "GREEN",
    "problem_color": "RED"
  }}
}}
```"""
        try:
            response = self.client.messages.create(
                model=config.MODEL,
                max_tokens=4000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.content[0].text
            match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
        except Exception as e:
            print(f"  ⚠️  Narrative planning error: {e}")
        
        return self._fallback_narrative()

    def _fallback_narrative(self) -> Dict:
        """Fallback narrative"""
        return {
            "hook": {"title": "The Problem", "problem": "Research challenge", "why_care": "Important", "visual_idea": "Problem"},
            "context": {"title": "Background", "previous_attempts": "Prior work", "limitations": "Limitations", "visual_idea": "Context"},
            "insight": {"title": "Key Insight", "aha_moment": "Core innovation", "why_clever": "Novel", "visual_idea": "Breakthrough"},
            "mechanism": [
                {"title": "Mechanism Overview", "explanation": "How it works", "visual_idea": "System"},
                {"title": "Technical Details", "explanation": "Implementation", "visual_idea": "Details"}
            ],
            "validation": {"title": "Results", "key_result": "Experimental results", "comparison": "Performance", "visual_idea": "Charts"},
            "implications": {"title": "Impact", "unlocks": "New possibilities", "broader_impact": "Advancement", "visual_idea": "Future"},
            "conclusion": {"title": "Conclusion", "future_work": "Next steps", "callback": "Solves problem", "visual_idea": "Summary"},
            "theme": {"main_concept_color": "BLUE", "comparison_color": "ORANGE", "result_color": "GREEN", "problem_color": "RED"}
        }