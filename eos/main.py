from analyzer import PaperAnalyzer
from planner import VideoPlanner
from generator import ManimGenerator  # Using the optimized generator
from pathlib import Path
import settings as cfg
import re
import fitz  # PyMuPDF
import subprocess
import sys

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        # Clean up text
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        raise

def process_pdf_to_video(pdf_path: Path) -> tuple[Path, str]:
    """
    Main pipeline: PDF -> Text -> Analysis -> Plan -> Code -> File
    Returns the path to the generated script file and the scene name.
    """
    
    # --- 1. SETUP ---
    analyzer = PaperAnalyzer()
    planner = VideoPlanner()
    generator = ManimGenerator()  # Using optimized generator with validation
    
    # Create a unique output directory for this paper
    paper_name = pdf_path.stem
    video_output_dir = cfg.OUTPUT_DIR / paper_name
    video_output_dir.mkdir(parents=True, exist_ok=True)
    
    # --- 2. EXTRACT ---
    print(f"\n[1/5] Extracting text from {pdf_path.name}...")
    paper_text = extract_text_from_pdf(pdf_path)
    print(f"  ✓ Extracted {len(paper_text)} characters")
    
    # --- 3. ANALYZE ---
    print(f"\n[2/5] Analyzing paper (this may take a moment)...")
    analysis = analyzer.analyze(paper_text)
    print(f"  ✓ Found {len(analysis.get('concepts', []))} key concepts")
    
    # --- 4. PLAN ---
    print(f"\n[3/5] Planning video script...")
    videos = planner.plan_videos(analysis)
    video = videos[0]  # Assuming one video
    print(f"  ✓ Created {len(video.scenes)} scenes")
    
    # --- 5. GENERATE ---
    print(f"\n[4/5] Generating Manim script with validation...")
    script_filepath = generator.generate_video_file(video, video_output_dir)
    scene_name = f"Video{video.number}"
    
    print(f"\n✅ Script generation complete: {script_filepath}")
    return Path(script_filepath), scene_name

def render_manim_video(script_path: Path, scene_name: str, quality: str = "l") -> bool:
    """
    Render the Manim video with proper error handling
    
    Args:
        script_path: Path to the generated Python script
        scene_name: Name of the scene class to render
        quality: Render quality (l=low, m=medium, h=high, p=production)
    
    Returns:
        True if successful, False otherwise
    """
    print(f"\n[5/5] Rendering video (quality={quality})...")
    
    cmd = [
        "python3", "-m", "manim", 
        "render",
        f"-q{quality}",  # Quality flag
        "--disable_caching",  # Avoid cache issues
        str(script_path),
        scene_name
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("\n🎉 SUCCESS! Video rendered successfully!")
            print(f"  ✓ Check the media folder for your video")
            return True
        else:
            print("\n⚠️ Render failed. Error details:")
            print("STDERR:", result.stderr)
            print("STDOUT:", result.stdout)
            
            # Try to identify common issues
            if "ModuleNotFoundError" in result.stderr:
                print("\n💡 Hint: Missing module. Try: pip install manim manim-voiceover")
            elif "AttributeError" in result.stderr:
                print("\n💡 Hint: API mismatch detected. Generator validation may need update.")
            elif "ELEVENLABS_API_KEY" in result.stderr:
                print("\n💡 Hint: Set ELEVENLABS_API_KEY environment variable")
                
            return False
            
    except subprocess.TimeoutExpired:
        print("\n⚠️ Rendering timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"\n🚨 Unexpected error during rendering: {e}")
        return False

def main():
    """Main entry point with enhanced error handling"""
    
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py /path/to/your.pdf [quality]")
        print("Quality options: l (low), m (medium), h (high), p (production)")
        print("Default: l (low quality for faster preview)")
        sys.exit(1)
    
    pdf_file_path = Path(sys.argv[1])
    quality = sys.argv[2] if len(sys.argv) > 2 else "l"
    
    # Validate input
    if not pdf_file_path.exists():
        print(f"❌ Error: File not found at {pdf_file_path}")
        sys.exit(1)
    
    if not pdf_file_path.suffix.lower() == '.pdf':
        print(f"❌ Error: File must be a PDF (got {pdf_file_path.suffix})")
        sys.exit(1)
    
    print(f"🚀 ConceptCast Pipeline Starting")
    print(f"📄 Input: {pdf_file_path.name}")
    print(f"🎬 Quality: {quality}")
    print("="*60)
    
    try:
        # Run the complete pipeline
        script_path, scene_name = process_pdf_to_video(pdf_file_path)
        
        # Attempt to render
        success = render_manim_video(script_path, scene_name, quality)
        
        if not success:
            print("\n🔧 Troubleshooting Tips:")
            print("1. Check that all dependencies are installed:")
            print("   pip install manim manim-voiceover elevenlabs anthropic")
            print("2. Verify environment variables are set:")
            print("   export ANTHROPIC_KEY='your-key'")
            print("   export ELEVENLABS_API_KEY='your-key'")
            print("3. Try running the generated script manually:")
            print(f"   python3 -m manim render -ql {script_path} {scene_name}")
            print("4. Check the generated code for issues:")
            print(f"   cat {script_path}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n🚨 Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 Debug info:")
        print(f"Working directory: {Path.cwd()}")
        print(f"Output directory: {cfg.OUTPUT_DIR}")
        print(f"Python version: {sys.version}")
        sys.exit(1)

if __name__ == '__main__':
    main()