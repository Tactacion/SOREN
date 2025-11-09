# api/doubt_clearing.py
"""
API endpoint for interactive doubt-clearing
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import anthropic
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from context.extractor import VideoContextExtractor
from settings import cfg

# Pydantic models
class DoubtRequest(BaseModel):
    job_id: str
    video_number: int
    timestamp: float
    question: str
    context_window: int = 15

class DoubtResponse(BaseModel):
    answer: str
    scene_info: dict
    timestamp: float
    sources: list


# Create FastAPI app
doubt_app = FastAPI()

# Enable CORS
doubt_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Anthropic client
client = anthropic.Anthropic(api_key=cfg.ANTHROPIC_KEY)


@doubt_app.post("/ask-doubt", response_model=DoubtResponse)
async def ask_doubt(request: DoubtRequest):
    """
    Answer a question about the video at specific timestamp
    """
    try:
        # Extract context
        output_dir = cfg.OUTPUT_DIR / request.job_id
        if not output_dir.exists():
            raise HTTPException(status_code=404, detail="Video not found")
        
        extractor = VideoContextExtractor(output_dir)
        context = extractor.extract_context(
            request.video_number,
            request.timestamp,
            request.context_window
        )
        
        # Build prompt for Claude
        prompt = _build_claude_prompt(request.question, context)
        
        # Get answer from Claude
        answer = _get_claude_answer(prompt, context.get('current_frame'))
        
        # Store Q&A for history (optional)
        # _store_qa(request, answer)
        
        return DoubtResponse(
            answer=answer,
            scene_info=context['scene_info'],
            timestamp=request.timestamp,
            sources=[
                f"Scene {context['scene_info']['scene_id']}: {context['scene_info']['scene_title']}",
                f"Video: {context['video_title']}"
            ]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _build_claude_prompt(question: str, context: dict) -> str:
    """Build comprehensive prompt for Claude"""
    
    scene_info = context['scene_info']
    scene_context = context['scene_context']
    
    prompt = f"""You are an expert AI tutor helping a student understand a technical video about:
"{context['video_title']}"

The student paused the video at {context['timestamp']:.1f} seconds and has a question.

=== CURRENT SCENE (Scene {scene_info['scene_id']}) ===
Title: {scene_info['scene_title']}

Narration (what was being said):
\"\"\"{scene_info['narration']}\"\"\"

Visual Instructions (what was being shown):
\"\"\"{scene_info.get('visual_instructions', 'N/A')}\"\"\"

=== CONTEXT FROM PREVIOUS SCENE ===
{_format_scene(scene_context.get('previous_scene'))}

=== CONTEXT FROM NEXT SCENE ===
{_format_scene(scene_context.get('next_scene'))}

=== ANIMATION CODE (Manim) ===
```python
{context.get('manim_code', 'N/A')[:2000]}  # Truncated if too long
```

=== PAPER CONCEPTS ===
{_format_concepts(context.get('analysis', {}).get('concepts', []))}

=== STUDENT'S QUESTION ===
"{question}"

=== YOUR TASK ===
Answer the student's question clearly and helpfully. Consider:
1. What's currently on screen (use the frame image I'll provide)
2. What was just explained (narration + previous scene)
3. The visual animations being shown
4. The underlying technical concepts from the paper

Provide a clear, educational answer that helps them understand. Use analogies and examples where helpful.
"""
    
    return prompt


def _format_scene(scene: Optional[dict]) -> str:
    """Format scene info for prompt"""
    if not scene:
        return "N/A"
    
    return f"""Title: {scene.get('title', 'N/A')}
Narration: {scene.get('narration', 'N/A')[:200]}..."""


def _format_concepts(concepts: list[dict]) -> str:
    """Format concepts for prompt"""
    if not concepts:
        return "N/A"
    
    formatted = []
    for c in concepts[:5]:  # Top 5 concepts
        formatted.append(f"- {c.get('name', '')}: {c.get('intuition', '')}")
    
    return '\n'.join(formatted)


def _get_claude_answer(prompt: str, frame_base64: Optional[str]) -> str:
    """Get answer from Claude with vision"""
    
    # Build message content
    content = []
    
    # Add frame image if available
    if frame_base64:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": frame_base64
            }
        })
    
    # Add text prompt
    content.append({
        "type": "text",
        "text": prompt
    })
    
    # Call Claude
    response = client.messages.create(
        model=cfg.MODEL,
        max_tokens=2000,
        temperature=0.3,  # Lower for educational accuracy
        messages=[{
            "role": "user",
            "content": content
        }]
    )
    
    return response.content[0].text


# Health check
@doubt_app.get("/health")
async def health():
    return {"status": "ok", "service": "doubt-clearing-api"}