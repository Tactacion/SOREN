# video_tools.py
# ============================================================================
# PROFESSIONAL-GRADE VIDEO GENERATION TOOLS FOR DEDALUS AGENT
# ============================================================================
# This module defines all the tools that our Dedalus agent can use.
# Each tool has:
# - Clear, comprehensive docstrings (used by Dedalus for tool descriptions)
# - Robust error handling with detailed error messages
# - Logging for debugging and monitoring
# - Type hints for clarity
# - Proper return value formatting

import anthropic
import settings as cfg
import json
import re
import fitz  # PyMuPDF
import subprocess
import logging
from pathlib import Path
from models import Video, Scene
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import our comprehensive knowledge base
from manim_knowledge import MANIM_API_KNOWLEDGE, MANIM_ERROR_DATABASE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(funcName)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Anthropic client for all LLM calls within tools
tool_client = anthropic.Anthropic(api_key=cfg.ANTHROPIC_KEY)

# ============================================================================
# TOOL 1: PDF TEXT EXTRACTION
# ============================================================================

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text content from a PDF file using PyMuPDF.

    This tool opens the PDF at the specified path, extracts text from every page,
    and returns the combined text as a single string with whitespace normalized.

    Args:
        pdf_path: Absolute path to the PDF file to extract text from

    Returns:
        Extracted text content as a single string, or error message if extraction fails

    Example:
        text = extract_text_from_pdf("/path/to/paper.pdf")

    Note:
        - Returns normalized text with excess whitespace removed
        - Handles multi-page PDFs automatically
        - Creates upload directory if it doesn't exist
    """
    logger.info(f"Starting PDF extraction from: {pdf_path}")

    try:
        # Ensure uploads directory exists
        cfg.UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

        # Validate file exists
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            error_msg = f"PDF_EXTRACTION_FAILED: File not found at {pdf_path}"
            logger.error(error_msg)
            return error_msg

        # Extract text from all pages
        doc = fitz.open(pdf_path)
        text = ""
        for page_num, page in enumerate(doc, 1):
            page_text = page.get_text()
            text += page_text
            logger.debug(f"Extracted {len(page_text)} chars from page {page_num}")

        doc.close()

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        logger.info(f"✅ Successfully extracted {len(text)} characters from {len(doc)} pages")
        return text

    except Exception as e:
        error_msg = f"PDF_EXTRACTION_FAILED: {type(e).__name__}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


# ============================================================================
# TOOL 2: PAPER ANALYZER (3Blue1Brown Style)
# ============================================================================

def analyze_paper(text: str) -> str:
    """
    Analyzes research paper text and extracts narrative structure for video creation.

    This tool uses Claude to deeply analyze a research paper and extract the key
    concepts, intuitions, and narrative arc needed to create an engaging 3Blue1Brown-style
    educational video. It focuses on the STORY and INTUITION rather than just facts.

    Args:
        text: Full text content extracted from the research paper

    Returns:
        JSON string containing structured analysis with title, hook, problem,
        key insight, and 12 key concepts. Returns error message if analysis fails.

    Example:
        analysis_json = analyze_paper(paper_text)
        analysis = json.loads(analysis_json)
        print(analysis['title'])

    Note:
        - Extracts 12 key concepts for comprehensive coverage
        - Each concept includes: hook, analogy, core_idea, visual_idea
        - Focuses on intuition and why things work, not just what they are
        - Uses temperature 0.4 for creative but consistent analysis
    """
    logger.info("Starting paper analysis for video narrative extraction")

    # Truncate text if too long (Claude has token limits)
    max_chars = 40000
    truncated_text = text[:max_chars]
    if len(text) > max_chars:
        logger.warning(f"Truncated paper text from {len(text)} to {max_chars} characters")

    prompt = f"""You are a world-class educational content creator specializing in 3Blue1Brown-style videos.
Your task is to analyze this research paper and extract the NARRATIVE STRUCTURE for an engaging video.

<paper_text>
{truncated_text}
</paper_text>

**YOUR MISSION:**
Transform this paper into a compelling STORY. Think like Grant Sanderson (3Blue1Brown):
- What's the hook that makes viewers care?
- What intuition can we build before showing formulas?
- What analogies make complex ideas click?
- What visual metaphors would illuminate the concepts?

**EXTRACT EXACTLY 12 KEY CONCEPTS** that build on each other to tell the complete story.

For each concept provide:
- **id**: Sequential number (1-12)
- **title**: Short, intriguing title (3-5 words)
- **hook**: The "why should I care?" question this answers (1 sentence)
- **analogy**: A real-world metaphor that builds intuition (1-2 sentences)
- **core_idea**: The actual concept explained intuitively (2-3 sentences)
- **why_it_works**: The insight that makes it brilliant (1-2 sentences)
- **visual_idea**: Concrete visual steps to animate this (2-3 specific visual actions)
- **builds_to**: What concept this leads into (concept title or "conclusion")

Return ONLY this JSON structure (no markdown, no extra text):
{{
  "title": "Simple, engaging paper title",
  "hook": "The intriguing opening question that hooks viewers",
  "problem": "What's broken or missing in current approaches",
  "key_insight": "The ONE clever idea that makes this paper special",
  "why_clever": "Why this insight is brilliant and non-obvious",
  "concepts": [
    {{
      "id": 1,
      "title": "Concept Title",
      "hook": "Why this matters",
      "analogy": "Real-world metaphor",
      "core_idea": "Intuitive explanation",
      "why_it_works": "The insight",
      "visual_idea": "Concrete visual steps: 1) Show X, 2) Transform to Y, 3) Reveal Z",
      "builds_to": "Next concept title"
    }},
    ... (12 concepts total)
  ]
}}

CRITICAL: Return valid JSON only. No markdown code blocks, no explanation text."""

    try:
        logger.info("Calling Claude for paper analysis...")
        response = tool_client.messages.create(
            model=cfg.MODEL,
            max_tokens=8192,
            temperature=0.4,  # Creative but consistent
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text.strip()

        # Extract JSON from potential markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)

        # Validate it's proper JSON
        analysis = json.loads(content)

        # Validate structure
        required_keys = ['title', 'hook', 'problem', 'key_insight', 'why_clever', 'concepts']
        if not all(key in analysis for key in required_keys):
            raise ValueError(f"Missing required keys. Found: {list(analysis.keys())}")

        if len(analysis['concepts']) != 12:
            logger.warning(f"Expected 12 concepts, got {len(analysis['concepts'])}")

        logger.info(f"✅ Analysis complete: {len(analysis['concepts'])} concepts extracted")
        return json.dumps(analysis, indent=2)

    except json.JSONDecodeError as e:
        error_msg = f"ANALYSIS_FAILED: Invalid JSON returned - {str(e)}"
        logger.error(error_msg)
        logger.debug(f"Response content: {content[:500]}")
        return error_msg

    except Exception as e:
        error_msg = f"ANALYSIS_FAILED: {type(e).__name__}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


# ============================================================================
# TOOL 3: VIDEO SCRIPT PLANNER
# ============================================================================

def plan_video_script(analysis_json: str) -> str:
    """
    Creates a detailed scene-by-scene video script from paper analysis.

    This tool takes the narrative analysis and plans out exactly how the video will flow,
    scene by scene. Each scene gets specific narration text and detailed visual instructions
    for what Manim animations to create.

    Args:
        analysis_json: JSON string from analyze_paper containing concepts and structure

    Returns:
        JSON string with detailed video plan including scenes with narration and visuals.
        Returns error message if planning fails.

    Example:
        script_plan = plan_video_script(analysis_json)
        plan = json.loads(script_plan)
        for scene in plan['scenes']:
            print(scene['title'])

    Note:
        - Creates 12-15 scenes from the 12 concepts
        - Each scene has 5-15 seconds of narration
        - Visual instructions are detailed and specific
        - Scenes build on each other progressively
    """
    logger.info("Starting video script planning")

    try:
        analysis = json.loads(analysis_json)
    except json.JSONDecodeError as e:
        error_msg = f"PLANNING_FAILED: Invalid analysis JSON - {str(e)}"
        logger.error(error_msg)
        return error_msg

    prompt = f"""You are a professional video script writer for educational math/CS content.
Create a detailed scene-by-scene script for a 3Blue1Brown-style video.

<analysis>
{json.dumps(analysis, indent=2)}
</analysis>

**YOUR TASK:**
Transform these concepts into a flowing video script with 12-15 scenes.

**SCRIPT STRUCTURE:**
- Scene 1: Hook + Problem introduction
- Scenes 2-13: One scene per concept (or combine simple concepts)
- Scene 14: Synthesis + Final insight
- Scene 15: Conclusion + Call to action

**FOR EACH SCENE:**
- **id**: Sequential number starting at 1
- **title**: Clear scene title (3-6 words)
- **narration**: Natural, conversational narration text (5-15 seconds when spoken)
  * Use "you" and "we" to engage viewers
  * Pose questions before revealing answers
  * Build suspense and curiosity
  * Use simple language, avoid jargon
- **visual_instructions**: Detailed, specific Manim animation instructions
  * Start simple, build complexity
  * Specify exact objects (Circle, MathTex, Arrow, etc.)
  * Describe transformations and highlights
  * Use color to direct attention
  * Clean up old content before new sections
- **cleanup_previous**: true if we should fade out previous scene's objects, false otherwise

Return ONLY this JSON (no markdown):
{{
  "video_number": 1,
  "video_title": "Engaging title that hooks viewers",
  "theme": "color_theme",
  "scenes": [
    {{
      "id": 1,
      "title": "The Hook",
      "narration": "Natural spoken text here. Keep it conversational!",
      "visual_instructions": "Specific animation steps: Create blue circle, write equation E=mc^2, highlight the c^2 term in yellow",
      "cleanup_previous": false
    }},
    ... (12-15 scenes total)
  ]
}}

CRITICAL: Natural narration, specific visual instructions, valid JSON only."""

    try:
        logger.info("Calling Claude for script planning...")
        response = tool_client.messages.create(
            model=cfg.MODEL,
            max_tokens=8192,
            temperature=0.5,  # More creative for narration
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text.strip()

        # Extract JSON
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)

        # Validate
        plan = json.loads(content)

        required_keys = ['video_number', 'video_title', 'theme', 'scenes']
        if not all(key in plan for key in required_keys):
            raise ValueError(f"Missing required keys. Found: {list(plan.keys())}")

        logger.info(f"✅ Script plan complete: {len(plan['scenes'])} scenes created")
        return json.dumps(plan, indent=2)

    except Exception as e:
        error_msg = f"PLANNING_FAILED: {type(e).__name__}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


# ============================================================================
# TOOL 4: MANIM CODE GENERATOR
# ============================================================================

def generate_manim_file(script_plan_json: str, paper_name: str) -> str:
    """
    Generates complete, executable Manim Python code from the video script plan.

    This tool takes the detailed script plan and generates actual Manim code that
    can be rendered into a video. It includes comprehensive Manim API knowledge
    to avoid common errors and create high-quality 3Blue1Brown-style animations.

    Args:
        script_plan_json: JSON string from plan_video_script with scenes and instructions
        paper_name: Safe filename for the paper (used for output file naming)

    Returns:
        JSON string with 'script_path' and 'scene_name' keys pointing to the
        generated Manim file. Returns error message if generation fails.

    Example:
        result = generate_manim_file(script_plan, "neural_networks")
        info = json.loads(result)
        render_video(info['script_path'], info['scene_name'])

    Note:
        - Uses comprehensive Manim 0.18.1 API knowledge
        - Avoids all forbidden camera operations
        - Includes proper voiceover integration
        - Generates clean, well-structured code
        - Saves to output directory automatically
    """
    logger.info(f"Starting Manim code generation for: {paper_name}")

    try:
        plan = json.loads(script_plan_json)
    except json.JSONDecodeError as e:
        error_msg = f"GENERATION_FAILED: Invalid script plan JSON - {str(e)}"
        logger.error(error_msg)
        return error_msg

    # Prepare output path
    output_dir = cfg.OUTPUT_DIR / paper_name
    output_dir.mkdir(exist_ok=True, parents=True)
    script_path = output_dir / f"{paper_name}_video.py"
    scene_name = f"Video{plan['video_number']}"

    logger.info(f"Output will be written to: {script_path}")

    prompt = f"""You are an EXPERT Manim 0.18.1 code generator specializing in VoiceoverScene.

**COMPREHENSIVE MANIM API KNOWLEDGE:**
{MANIM_API_KNOWLEDGE}

**VIDEO SCRIPT TO IMPLEMENT:**
{json.dumps(plan, indent=2)}

**YOUR TASK:**
Generate a complete, executable Manim script that brings this video to life.

**REQUIREMENTS:**
1. Use VoiceoverScene as the base class
2. Implement ALL scenes with proper voiceover integration
3. Follow the exact visual instructions for each scene
4. Use ONLY allowed Manim API methods (check FORBIDDEN_API list!)
5. Create beautiful, smooth 3Blue1Brown-style animations
6. Proper cleanup between major scene transitions

**CODE STRUCTURE:**
```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
import numpy as np

class {scene_name}(VoiceoverScene):
    def construct(self):
        # Setup voiceover service
        self.set_speech_service(
            ElevenLabsService(
                api_key="{cfg.ELEVENLABS_API_KEY}",
                voice="Adam"
            )
        )

        # Scene 1
        with self.voiceover(text=\"Scene 1 narration here\") as tracker:
            # Visual animations for scene 1
            title = Text("Title")
            self.play(Write(title))
            self.wait(tracker.get_remaining_duration())

        # Cleanup before next major section
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)

        # Scene 2
        with self.voiceover(text=\"Scene 2 narration\") as tracker:
            # More animations
            ...

        # ... implement ALL scenes
```

**CRITICAL RULES:**
- NO camera operations (self.camera.*, move_camera, etc.)
- NO .animate methods except: scale, shift, move_to, rotate, set_color, set_opacity, set_fill, set_stroke, align_to, next_to
- ALL Text/MathTex inputs must be str() wrapped if uncertain
- Use Group(*self.mobjects) not VGroup(*self.mobjects)
- Clean up between major sections with FadeOut
- Match animation timing to narration duration

Return ONLY the Python code. No markdown code blocks, no explanation."""

    try:
        logger.info("Calling Claude for Manim code generation...")
        response = tool_client.messages.create(
            model=cfg.MODEL,
            max_tokens=16000,  # Longer code needs more tokens
            temperature=0.3,  # Low temp for precise code generation
            messages=[{"role": "user", "content": prompt}]
        )

        code = response.content[0].text.strip()

        # Extract code from markdown if present
        code_match = re.search(r'```(?:python)?\s*\n(.*?)```', code, re.DOTALL)
        if code_match:
            code = code_match.group(1)

        # Validate it looks like Python code
        if not code.startswith("from manim import"):
            logger.warning("Generated code doesn't start with expected imports")

        # Write to file
        script_path.write_text(code, encoding='utf-8')

        logger.info(f"✅ Manim code generated: {len(code)} characters written to {script_path}")

        return json.dumps({
            "script_path": str(script_path),
            "scene_name": scene_name
        })

    except Exception as e:
        error_msg = f"GENERATION_FAILED: {type(e).__name__}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


# ============================================================================
# TOOL 5: VIDEO RENDERER
# ============================================================================

def render_video(script_path: str, scene_name: str) -> str:
    """
    Renders the Manim script into an actual MP4 video file.

    This tool executes the Manim rendering command on the generated Python script.
    It captures all output and returns either the path to the rendered video or
    a detailed error message if rendering fails.

    Args:
        script_path: Absolute path to the Manim Python script file
        scene_name: Name of the Scene class to render (e.g., "Video1")

    Returns:
        Path to rendered MP4 file if successful, or "RENDER_FAILED: <traceback>"
        if rendering crashes. The traceback can be passed to fix_manim_script.

    Example:
        result = render_video("/path/to/script.py", "Video1")
        if result.startswith("RENDER_FAILED:"):
            fix_manim_script(script_path, result)
        else:
            print(f"Video ready: {result}")

    Note:
        - Uses -ql (low quality) for faster iteration
        - Captures both stdout and stderr
        - Includes full traceback on failure for debugging
        - Returns parseable error format for fix_manim_script tool
    """
    logger.info(f"Starting render: {scene_name} from {script_path}")

    try:
        # Validate script file exists
        if not Path(script_path).exists():
            error_msg = f"RENDER_FAILED: Script file not found at {script_path}"
            logger.error(error_msg)
            return error_msg

        # Run manim render command
        cmd = ["python", "-m", "manim", "render", "-ql", str(script_path), scene_name]
        logger.info(f"Executing: {' '.join(cmd)}")

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=600  # 10 minute timeout
        )

        # Check for success
        if process.returncode == 0:
            logger.info("✅ Render successful!")
            logger.debug(f"Stdout: {process.stdout[-500:]}")  # Last 500 chars

            # Extract video path from output
            # Manim typically outputs: "File ready at /path/to/video.mp4"
            video_path_match = re.search(r'File ready at (.+\.mp4)', process.stdout)
            if video_path_match:
                video_path = video_path_match.group(1).strip()
                logger.info(f"Video file: {video_path}")
                return video_path
            else:
                # Fallback: construct expected path
                script_dir = Path(script_path).parent
                media_dir = script_dir / "media" / "videos"
                # Search for the most recent MP4
                mp4_files = list(media_dir.rglob("*.mp4"))
                if mp4_files:
                    most_recent = max(mp4_files, key=lambda p: p.stat().st_mtime)
                    logger.info(f"Found video file: {most_recent}")
                    return str(most_recent)
                else:
                    logger.warning("Could not locate output video file")
                    return f"Render completed but video path not found. Check {media_dir}"

        # Render failed - return detailed error
        error_msg = f"RENDER_FAILED:\n{process.stderr}"
        logger.error(f"Render failed with return code {process.returncode}")
        logger.debug(f"Stderr: {process.stderr}")
        return error_msg

    except subprocess.TimeoutExpired:
        error_msg = "RENDER_FAILED: Rendering timeout after 10 minutes"
        logger.error(error_msg)
        return error_msg

    except Exception as e:
        error_msg = f"RENDER_FAILED: {type(e).__name__}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


# ============================================================================
# TOOL 6: MANIM SCRIPT FIXER
# ============================================================================

def fix_manim_script(script_path: str, traceback: str) -> str:
    """
    Automatically fixes Manim code errors using error traceback analysis.

    This tool takes a failing Manim script and its error traceback, analyzes the
    error using comprehensive Manim error database knowledge, and generates a fix.
    The fixed code is written back to the same file, ready for re-rendering.

    Args:
        script_path: Absolute path to the Manim script that failed to render
        traceback: Error traceback string (typically from render_video's RENDER_FAILED output)

    Returns:
        The script_path string to indicate the file has been fixed and is ready
        for retry. Returns error message if fixing fails.

    Example:
        result = render_video(script_path, scene_name)
        if result.startswith("RENDER_FAILED:"):
            fix_manim_script(script_path, result)
            result = render_video(script_path, scene_name)  # Retry

    Note:
        - Uses comprehensive error database for precise fixes
        - Fixes ONLY the specific error, preserves all other code
        - Does not add features or rewrite working code
        - Uses low temperature (0.1) for deterministic fixes
        - Should be called in a retry loop with max 3 attempts
    """
    logger.info(f"Starting code fix for: {script_path}")
    logger.info(f"Error traceback length: {len(traceback)} characters")

    try:
        # Read the broken code
        script_file = Path(script_path)
        if not script_file.exists():
            error_msg = f"FIX_FAILED: Script file not found at {script_path}"
            logger.error(error_msg)
            return error_msg

        current_code = script_file.read_text(encoding='utf-8')
        logger.debug(f"Current code length: {len(current_code)} characters")

        # Remove "RENDER_FAILED:" prefix if present
        clean_traceback = traceback.replace("RENDER_FAILED:", "").strip()

        prompt = f"""You are a SPECIALIST Manim 0.18.1 debugging agent.

**COMPREHENSIVE ERROR DATABASE:**
{MANIM_ERROR_DATABASE}

**BROKEN CODE:**
<bad_code>
{current_code}
</bad_code>

**ERROR TRACEBACK:**
<traceback>
{clean_traceback}
</traceback>

**YOUR TASK:**
Fix this code using the ERROR_DATABASE as your guide.

**DEBUGGING WORKFLOW:**
1. Read the traceback and find the exact line number that crashed
2. Identify the error type (TypeError, AttributeError, ValueError, etc.)
3. Search the ERROR_DATABASE for this error pattern
4. Apply the EXACT solution from the database
5. Return the COMPLETE fixed code

**CRITICAL RULES:**
- Fix ONLY the specific error mentioned in the traceback
- Do NOT change any other code
- Do NOT add new features or "improvements"
- Do NOT rewrite working sections
- Do NOT add explanatory comments
- Preserve the original code structure exactly
- Use ONLY the allowed Manim API methods

**OUTPUT:**
Return the COMPLETE fixed Python code. No markdown blocks, no explanations, just code."""

        logger.info("Calling Claude for code fix...")
        response = tool_client.messages.create(
            model=cfg.FIXER_MODEL,
            max_tokens=16000,
            temperature=0.1,  # Very low for deterministic fixes
            messages=[{"role": "user", "content": prompt}]
        )

        fixed_code = response.content[0].text.strip()

        # Extract code from markdown if present
        code_match = re.search(r'```(?:python)?\s*\n(.*?)```', fixed_code, re.DOTALL)
        if code_match:
            fixed_code = code_match.group(1)

        # Validate it looks like Python
        if not fixed_code.startswith("from manim import"):
            logger.warning("Fixed code doesn't start with expected imports")

        # Write the fix back to the same file
        script_file.write_text(fixed_code, encoding='utf-8')

        logger.info(f"✅ Code fixed and saved to {script_path}")
        logger.info(f"Fixed code length: {len(fixed_code)} characters")

        return str(script_path)

    except Exception as e:
        error_msg = f"FIX_FAILED: {type(e).__name__}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


# ============================================================================
# TOOL REGISTRY (for easy import)
# ============================================================================

ALL_TOOLS = [
    extract_text_from_pdf,
    analyze_paper,
    plan_video_script,
    generate_manim_file,
    render_video,
    fix_manim_script
]

if __name__ == "__main__":
    # Module test
    logger.info("video_tools module loaded successfully")
    logger.info(f"Available tools: {[tool.__name__ for tool in ALL_TOOLS]}")
