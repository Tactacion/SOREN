# equation_extractor.py - RELIABLE EQUATION EXTRACTION

import anthropic
import re
import json
from typing import List, Dict
import config

class EquationExtractor:
    """Extract equations reliably from PDF text"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_KEY)
    
    def extract_from_text(self, text: str) -> List[Dict]:
        """Extract LaTeX equations from raw text"""
        
        equations = []
        
        # Pattern 1: $...$
        inline = r'\$([^\$]{3,})\$'
        for match in re.finditer(inline, text):
            latex = match.group(1).strip()
            equations.append({'latex': latex, 'type': 'inline'})
        
        # Pattern 2: $$...$$
        display = r'\$\$([^\$]+)\$\$'
        for match in re.finditer(display, text):
            latex = match.group(1).strip()
            equations.append({'latex': latex, 'type': 'display'})
        
        # Pattern 3: \begin{equation}...\end{equation}
        env = r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}'
        for match in re.finditer(env, text, re.DOTALL):
            latex = match.group(1).strip()
            equations.append({'latex': latex, 'type': 'equation'})
        
        # Pattern 4: \begin{align}...\end{align}
        align = r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}'
        for match in re.finditer(align, text, re.DOTALL):
            latex = match.group(1).strip()
            equations.append({'latex': latex, 'type': 'align'})
        
        # Deduplicate and filter
        seen = set()
        unique = []
        for eq in equations:
            normalized = self._normalize(eq['latex'])
            if normalized not in seen and len(normalized) > 5:
                seen.add(normalized)
                unique.append(eq)
        
        # Get explanations for top 15
        return self._explain_equations(unique[:15])
    
    def _normalize(self, latex: str) -> str:
        """Normalize for deduplication"""
        latex = re.sub(r'\s+', ' ', latex)
        latex = re.sub(r'\\label\{[^}]+\}', '', latex)
        return latex.strip()
    
    def _explain_equations(self, equations: List[Dict]) -> List[Dict]:
        """Get explanations from LLM"""
        
        if not equations:
            return []
        
        eq_list = "\n".join([f"{i+1}. {eq['latex']}" for i, eq in enumerate(equations)])
        
        prompt = f"""Explain these equations extracted from a paper.

EQUATIONS:
{eq_list}

For each, provide:
- description: One sentence explanation
- variables: Dict of variable meanings (if clear)

Return JSON:
{{
  "equations": [
    {{"latex": "...", "description": "...", "variables": {{}}}}
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=config.MODEL,
                max_tokens=4000,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            
            json_match = re.search(r'\{.*\}', response.content[0].text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get('equations', [])
        except:
            pass
        
        # Fallback
        return [{'latex': eq['latex'], 'description': '', 'variables': {}} for eq in equations]
    
    def escape_for_manim(self, latex: str) -> str:
        """Escape LaTeX for Manim MathTex"""
        # Double backslashes
        latex = latex.replace('\\', '\\\\')
        # Double braces
        latex = latex.replace('{', '{{').replace('}', '}}')
        return latex