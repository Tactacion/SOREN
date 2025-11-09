"""
Doubt Handler - EOS Backend Integration
Generates concise, purpose-driven responses using Gemini
"""
import google.generativeai as genai
from typing import Dict, Optional, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DoubtHandler:
    """
    Handle student questions with concise, purpose-driven Gemini responses
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment. Add it to your .env file.")

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Use Gemini 2.0 Flash for best vision + speed
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def answer_question(
        self,
        question: str,
        context: Dict,
        style: str = "educational"
    ) -> Dict:
        """
        Generate CONCISE answer to student question using full context

        Args:
            question: Student's question
            context: Rich context from VideoContextExtractor
            style: Response style (educational/technical/intuitive)

        Returns:
            Dict with answer, sources, and metadata
        """
        # Build the PERFECT concise prompt
        prompt = self._build_concise_prompt(question, context, style)

        # Build content with multiple frames
        content = self._build_multimodal_content(prompt, context)

        # Call Gemini
        try:
            response = self.model.generate_content(
                content,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=300,  # FORCE conciseness
                )
            )

            answer_text = response.text

            return {
                'answer': answer_text,
                'sources': self._build_sources(context),
                'context_used': {
                    'section': context['section_info']['title'],
                    'timestamp': context['timestamp'],
                    'frames_used': len(context.get('frames', [])),
                },
                'tokens_used': response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
            }

        except Exception as e:
            return {
                'answer': f"Error: {str(e)}",
                'sources': [],
                'context_used': {},
                'error': str(e)
            }

    def _build_concise_prompt(
        self,
        question: str,
        context: Dict,
        style: str
    ) -> str:
        """
        THE PERFECT PROMPT - Concise, purpose-driven, NO meta-talk
        """

        # Extract key context
        current_vo = context.get('voiceover_text', 'No voiceover available')
        section = context['section_info']
        concepts = context.get('key_concepts', [])

        # Get extra context (PDF and Manim code)
        # Try extra_pdf_text first (from demo mode), then fallback to pdf_text from context_extractor
        pdf_text = context.get('extra_pdf_text', '') or context.get('pdf_text', '')
        manim_code = context.get('extra_manim_code', '') or context.get('manim_code', '')

        # Format concepts
        concepts_text = ', '.join([
            c.get('name', c) if isinstance(c, dict) else c
            for c in concepts[:3]
        ]) if concepts else 'core concepts'

        # Build additional context sections
        extra_context_section = ""
        has_frames = len(context.get('frames', [])) > 0

        if pdf_text:
            # Use more PDF text if we don't have frames
            pdf_limit = 2000 if not has_frames else 500
            extra_context_section += f"\n- Source Material: {pdf_text[:pdf_limit]}..."

        if manim_code:
            # Extract relevant scene names from Manim code
            manim_preview = manim_code[:800] if len(manim_code) > 800 else manim_code
            extra_context_section += f"\n- Animation Details: {manim_preview}"

        # Adjust instructions based on whether we have frames
        visual_instruction = ""
        if has_frames:
            visual_instruction = "1. **Directly answer what they see** (reference the visual elements in the frames)\n"
        else:
            visual_instruction = "1. **Directly answer their question** based on the source material\n"

        prompt = f"""You are explaining a technical concept to a student.

**CONTEXT:**
- Topic: {section['title']}
- Current explanation: {current_vo[:150]}...
- Key concepts: {concepts_text}{extra_context_section}

**STUDENT'S QUESTION:** {question}

**YOUR TASK:**
Answer in 2-3 CONCISE sentences that:
{visual_instruction}2. **Explain the PURPOSE** (what is it FOR? why does it matter?)
3. **Connect to the end goal** (how does this help understand the topic?)

**CRITICAL RULES:**
- NO meta-commentary (don't mention "frames", "animation code", "timestamps", "narration", "source material")
- NO long explanations - be direct and concise
- ALWAYS explain the purpose/goal, not just what it is
- Use technical terms from the concepts list
{"- Be specific about what you see in the images" if has_frames else "- Use the source material to provide accurate context"}

Example good answer:
"These arrows represent the gradient flow field pointing toward high-density regions. They guide the diffusion process by showing where samples should move during denoising, which is essential for the model to generate realistic outputs."

Example BAD answer:
"Based on the animation code and narration at 25.7 seconds, you're seeing a transitional moment... [500 words of meta-talk]"

Answer now:"""

        return prompt

    def _build_multimodal_content(self, prompt: str, context: Dict) -> List:
        """
        Build content with multiple frames for Gemini
        """
        content = []

        # Add frames (simple base64 strings)
        frames = context.get('frames', [])

        if frames:
            # Add all frames
            for frame_base64 in frames:
                content.append({
                    'mime_type': 'image/jpeg',
                    'data': frame_base64
                })

        # Add text prompt AFTER images
        content.append(prompt)

        return content

    def _build_sources(self, context: Dict) -> List[str]:
        """Build source citations"""
        sources = [
            f"Section: {context['section_info']['title']}"
        ]

        if context.get('timestamp'):
            sources.append(f"Timestamp: {context['timestamp']:.1f}s")

        return sources
