# run_pipeline.py
# ============================================================================
# PROFESSIONAL DEDALUS LABS AGENTIC WORKFLOW ORCHESTRATOR
# ============================================================================
# This is the main orchestration script using Dedalus Labs MCP framework
# for ML paper to Manim video generation with advanced error handling,
# retry logic, and comprehensive agent prompting.

import asyncio
import settings as cfg
import re
import traceback
import sys
import logging
from pathlib import Path
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional

# Import all our tools
from video_tools import (
    extract_text_from_pdf,
    analyze_paper,
    plan_video_script,
    generate_manim_file,
    render_video,
    fix_manim_script,
    ALL_TOOLS
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(cfg.OUTPUT_DIR / 'pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# MAIN PIPELINE ORCHESTRATION
# ============================================================================

async def run_video_pipeline(pdf_path: str) -> Optional[str]:
    """
    Orchestrates the complete ML paper to Manim video pipeline using Dedalus Labs.

    This function manages a sophisticated agentic workflow that:
    1. Extracts text from PDF
    2. Analyzes paper for narrative structure
    3. Plans detailed video script
    4. Generates Manim code
    5. Renders video with automatic error fixing (up to 3 retries)

    Args:
        pdf_path: Absolute path to the ML/CS research paper PDF file

    Returns:
        Path to the final rendered MP4 video file, or None if pipeline fails

    Note:
        Uses Dedalus Runner for non-linear agentic workflow orchestration
        Includes comprehensive error handling and automatic retry logic
    """
    logger.info("="*80)
    logger.info(f"🎬 STARTING DEDALUS VIDEO PIPELINE")
    logger.info(f"📄 Input PDF: {pdf_path}")
    logger.info(f"🕐 Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*80)

    # Validate inputs
    pdf_file = Path(pdf_path).resolve()
    if not pdf_file.exists():
        logger.error(f"❌ PDF file not found: {pdf_path}")
        return None

    paper_name = re.sub(r'[^a-zA-Z0-9]', '_', pdf_file.stem)
    logger.info(f"📝 Paper name (sanitized): {paper_name}")

    # Initialize Dedalus client
    try:
        client = AsyncDedalus(api_key=cfg.DEDALUS_API_KEY)
        runner = DedalusRunner(client)
        logger.info("✅ Dedalus client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Dedalus: {e}")
        return None

    # ========================================================================
    # ADVANCED AGENT PROMPT
    # ========================================================================
    # This is the "Manager Agent" that orchestrates all the tools
    # Key improvements over basic version:
    # - More explicit error handling instructions
    # - Better step-by-step workflow description
    # - Clearer retry logic with max attempts
    # - More context about what each tool does and returns
    # ========================================================================

    prompt = f"""You are an EXPERT AI ENGINEER managing a complex video generation pipeline.

Your mission: Transform this PDF into a professional 3Blue1Brown-style Manim video.

**INPUT FILE:** '{str(pdf_file)}'
**PAPER NAME (for file naming):** '{paper_name}'

**YOUR TOOLS:**
You have access to 6 powerful tools, each with specific purposes:

1. **extract_text_from_pdf(pdf_path: str) -> str**
   - Extracts all text from the PDF
   - Returns: Full paper text, or "PDF_EXTRACTION_FAILED: ..." on error
   - Call this FIRST with the input file path

2. **analyze_paper(text: str) -> str**
   - Analyzes paper and extracts narrative structure
   - Returns: JSON string with 12 key concepts, hooks, analogies, visual ideas
   - Call this with the extracted text from step 1

3. **plan_video_script(analysis_json: str) -> str**
   - Creates detailed scene-by-scene video script
   - Returns: JSON with 12-15 scenes, each with narration and visual instructions
   - Call this with the analysis JSON from step 2

4. **generate_manim_file(script_plan_json: str, paper_name: str) -> str**
   - Generates executable Manim Python code
   - Returns: JSON with {{"script_path": "...", "scene_name": "..."}}
   - Call this with script plan from step 3 and paper_name '{paper_name}'

5. **render_video(script_path: str, scene_name: str) -> str**
   - Renders the Manim code into MP4 video
   - Returns: Path to MP4 if successful, or "RENDER_FAILED: <traceback>" if crash
   - Call this with script_path and scene_name from step 4

6. **fix_manim_script(script_path: str, traceback: str) -> str**
   - Automatically fixes Manim code errors
   - Returns: script_path (indicating file is fixed and ready to retry)
   - Call this ONLY if render_video returns "RENDER_FAILED: ..."

**EXECUTION WORKFLOW:**

PHASE 1: Content Processing (Steps 1-4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: Extract PDF text
- Call: extract_text_from_pdf('{str(pdf_file)}')
- Check: If result starts with "PDF_EXTRACTION_FAILED:", STOP and report error
- Otherwise: Store result as `paper_text`

Step 2: Analyze paper narrative
- Call: analyze_paper(paper_text)
- Check: If result starts with "ANALYSIS_FAILED:", STOP and report error
- Otherwise: Store result as `analysis_json`

Step 3: Plan video script
- Call: plan_video_script(analysis_json)
- Check: If result starts with "PLANNING_FAILED:", STOP and report error
- Otherwise: Store result as `script_plan_json`

Step 4: Generate Manim code
- Call: generate_manim_file(script_plan_json, '{paper_name}')
- Check: If result starts with "GENERATION_FAILED:", STOP and report error
- Otherwise: Parse the JSON to extract `script_path` and `scene_name`

PHASE 2: Render with Automatic Fix Loop (Step 5-6)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You will now enter a render-fix loop with MAX 3 attempts:

attempt = 1

LOOP START:
  Step 5: Attempt render
  - Call: render_video(script_path, scene_name)
  - Examine result:

  IF result DOES NOT start with "RENDER_FAILED:":
    ✅ SUCCESS! Result is the final MP4 path.
    - Output this path as your FINAL ANSWER
    - STOP (mission accomplished!)

  IF result DOES start with "RENDER_FAILED:":
    ⚠️ Render crashed. Check attempt counter:

    IF attempt >= 3:
      ❌ Max attempts reached. Report final error and STOP.

    IF attempt < 3:
      Step 6: Fix the code
      - Call: fix_manim_script(script_path, result)
        # result contains the full traceback
      - This overwrites script_path with fixed code
      - Increment attempt = attempt + 1
      - GOTO Step 5 (retry render)

**CRITICAL SUCCESS CRITERIA:**
- Follow the workflow EXACTLY in order
- Check each tool's return value for error prefixes
- Do NOT skip steps or guess values
- Do NOT try more than 3 render attempts
- Your FINAL output should be the MP4 video file path

**ERROR HANDLING:**
- If ANY tool returns an error (check for "*_FAILED:" prefix), STOP immediately and report
- Only exception: RENDER_FAILED triggers the fix-retry loop (max 3 times)

**STARTING INSTRUCTION:**
Begin now by calling extract_text_from_pdf('{str(pdf_file)}') and proceed through the workflow.
I'll be monitoring your progress. Good luck! 🚀"""

    # ========================================================================
    # RUN THE AGENT
    # ========================================================================

    try:
        logger.info("━" * 80)
        logger.info("🤖 LAUNCHING DEDALUS AGENT")
        logger.info("━" * 80)
        logger.info(f"Model: {cfg.MODEL}")
        logger.info(f"Tools available: {len(ALL_TOOLS)}")
        logger.info(f"Streaming: Disabled (waiting for final result)")
        logger.info("")

        start_time = datetime.now()

        result = await runner.run(
            input=prompt,
            model=cfg.MODEL,
            tools=ALL_TOOLS,
            stream=False  # Get final result, not streaming
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info("")
        logger.info("━" * 80)
        logger.info("🎉 DEDALUS AGENT COMPLETED")
        logger.info("━" * 80)
        logger.info(f"⏱️  Total duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        logger.info(f"📊 Final output: {result.final_output}")
        logger.info("━" * 80)

        # Extract video path from result
        final_output = result.final_output

        # Check if output looks like a path
        if isinstance(final_output, str) and ('.mp4' in final_output or '/media/' in final_output):
            video_path = final_output.strip()
            if Path(video_path).exists():
                logger.info(f"✅ Video file confirmed at: {video_path}")
                return video_path
            else:
                logger.warning(f"⚠️  Agent returned path but file not found: {video_path}")
                return None
        else:
            logger.warning(f"⚠️  Agent completed but output doesn't look like video path")
            logger.warning(f"Output: {final_output}")
            return None

    except Exception as e:
        logger.error("━" * 80)
        logger.error("❌ DEDALUS AGENT FAILED")
        logger.error("━" * 80)
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error(f"Full traceback:")
        logger.error(traceback.format_exc())
        logger.error("━" * 80)
        return None


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def validate_environment() -> bool:
    """
    Validates that all required environment variables and dependencies are present.

    Returns:
        True if environment is valid, False otherwise
    """
    logger.info("🔍 Validating environment...")

    errors = []

    # Check API keys
    if not cfg.DEDALUS_API_KEY:
        errors.append("DEDALUS_API_KEY not found in .env file")

    if not cfg.ANTHROPIC_KEY:
        errors.append("ANTHROPIC_API_KEY not found in .env file")

    if not cfg.ELEVENLABS_API_KEY:
        errors.append("ELEVENLABS_API_KEY not found in .env file")

    # Check directories
    if not cfg.OUTPUT_DIR.exists():
        logger.info(f"Creating output directory: {cfg.OUTPUT_DIR}")
        cfg.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not cfg.UPLOAD_DIR.exists():
        logger.info(f"Creating upload directory: {cfg.UPLOAD_DIR}")
        cfg.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Check Python imports
    try:
        import manim
        logger.info(f"✅ Manim version: {manim.__version__}")
    except ImportError:
        errors.append("Manim not installed. Run: pip install manim==0.18.1")

    try:
        import manim_voiceover
        logger.info(f"✅ Manim-voiceover installed")
    except ImportError:
        errors.append("Manim-voiceover not installed. Run: pip install manim-voiceover")

    try:
        from dedalus_labs import AsyncDedalus
        logger.info(f"✅ Dedalus Labs SDK installed")
    except ImportError:
        errors.append("Dedalus Labs not installed. Run: pip install dedalus-labs")

    if errors:
        logger.error("❌ Environment validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        return False

    logger.info("✅ Environment validation passed")
    return True


def main():
    """
    Main entry point for CLI usage.

    Usage:
        python run_pipeline.py /path/to/paper.pdf
    """
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║        🎬 ML PAPER TO MANIM VIDEO - DEDALUS AGENTIC WORKFLOW 🤖          ║
║                                                                           ║
║  Professional-grade video generation powered by Dedalus Labs + Claude    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")

    # Parse arguments
    if len(sys.argv) < 2:
        print("❌ Error: No PDF file specified")
        print()
        print("Usage:")
        print("  python run_pipeline.py /path/to/paper.pdf")
        print()
        print("Example:")
        print("  python run_pipeline.py ./papers/attention_is_all_you_need.pdf")
        print()
        sys.exit(1)

    pdf_file_path = sys.argv[1]

    # Validate file exists
    if not Path(pdf_file_path).exists():
        print(f"❌ Error: File not found at {pdf_file_path}")
        sys.exit(1)

    # Validate environment
    if not validate_environment():
        print("\n❌ Environment validation failed. Please fix the issues above.")
        sys.exit(1)

    # Run the pipeline
    print("\n" + "="*80)
    print("🚀 STARTING PIPELINE")
    print("="*80 + "\n")

    try:
        video_path = asyncio.run(run_video_pipeline(pdf_file_path))

        if video_path:
            print("\n" + "="*80)
            print("🎉 SUCCESS! VIDEO GENERATION COMPLETE!")
            print("="*80)
            print(f"\n📹 Your video is ready at:")
            print(f"   {video_path}")
            print(f"\n💡 You can now:")
            print(f"   - Play the video")
            print(f"   - Share it with others")
            print(f"   - Upload to YouTube/social media")
            print("\n" + "="*80 + "\n")
            sys.exit(0)
        else:
            print("\n" + "="*80)
            print("❌ PIPELINE FAILED")
            print("="*80)
            print("\n⚠️  The pipeline encountered errors.")
            print("📋 Check the logs above for details.")
            print(f"📝 Full log available at: {cfg.OUTPUT_DIR / 'pipeline.log'}")
            print("\n" + "="*80 + "\n")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user (Ctrl+C)")
        print("🛑 Shutting down gracefully...")
        sys.exit(130)

    except Exception as e:
        print("\n" + "="*80)
        print("💥 UNEXPECTED ERROR")
        print("="*80)
        print(f"\nError: {type(e).__name__}: {str(e)}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        print("\n" + "="*80 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
