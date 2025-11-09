import json
import re
import anthropic
from typing import Dict, List
from paper_to_video.generators.models import Concept, Scene, Video
import config

class PaperAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_KEY)
    
    def analyze(self, text: str) -> Video:
        concepts = self._extract_concepts(text)
        scenes = self._plan_scenes(concepts, text)
        
        return Video(
            title="Paper Explanation",
            concepts=concepts,
            scenes=scenes,
            total_duration=sum(s.duration for s in scenes)
        )
    
    def _extract_json(self, text: str) -> dict:
        """Extract JSON from Claude's response"""
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON in code blocks
        code_block = re.search(r'```(?:json)?\n?(.*?)\n?```', text, re.DOTALL)
        if code_block:
            try:
                return json.loads(code_block.group(1))
            except json.JSONDecodeError:
                pass
        
        # Last resort - try the whole text
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Could not extract JSON from response: {text[:200]}...")
    
    def _extract_concepts(self, text: str) -> Dict[str, Concept]:
        prompt = f"""Analyze this ML paper and extract 5-10 key concepts.

Paper text (first 5000 chars):
{text[:5000]}

Return ONLY valid JSON in this exact format:
{{
    "concepts": [
        {{
            "name": "concept_name",
            "description": "one line description",
            "dependencies": [],
            "visual_metaphor": "how to visualize this"
        }}
    ]
}}

Be precise and technical. Focus on the main algorithmic concepts."""
        
        response = self.client.messages.create(
            model=config.MODEL,
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        data = self._extract_json(response.content[0].text)
        concepts = {}
        for c in data.get('concepts', []):
            try:
                concepts[c['name']] = Concept(**c)
            except Exception as e:
                print(f"Warning: Skipping concept due to error: {e}")
        
        if not concepts:
            # Fallback concepts
            concepts = {
                "main_concept": Concept(
                    name="main_concept",
                    description="The main idea of the paper",
                    dependencies=[],
                    visual_metaphor="A flowing diagram"
                )
            }
        
        return concepts
    
    def _plan_scenes(self, concepts: Dict[str, Concept], text: str) -> List[Scene]:
        concept_list = "\n".join([f"- {k}: {v.description}" for k, v in concepts.items()])
        
        prompt = f"""Plan 5-8 scenes for a 3Blue1Brown-style video explaining these concepts:

{concept_list}

Paper context:
{text[:3000]}

Requirements:
- Each scene: 20-40 seconds
- Build complexity gradually
- Include visual metaphors
- Make it engaging

Return ONLY valid JSON:
{{
    "scenes": [
        {{
            "id": 1,
            "concepts": ["concept_name"],
            "narration": "Clear explanation in 2-3 sentences.",
            "duration": 30.0,
            "visuals": ["visual element 1", "visual element 2"]
        }}
    ]
}}"""
        
        response = self.client.messages.create(
            model=config.MODEL,
            max_tokens=3000,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}]
        )
        
        data = self._extract_json(response.content[0].text)
        scenes = []
        
        for s in data.get('scenes', []):
            try:
                scenes.append(Scene(**s))
            except Exception as e:
                print(f"Warning: Skipping scene due to error: {e}")
        
        if not scenes:
            # Fallback scene
            scenes = [Scene(
                id=1,
                concepts=list(concepts.keys())[:1],
                narration="Let's explore the main concept of this paper.",
                duration=30.0,
                visuals=["Title card", "Main diagram"]
            )]
        
        return scenes