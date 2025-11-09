#!/usr/bin/env python3
"""Paper to Video - Simple & Working"""

import sys
from pathlib import Path
import PyPDF2

from analyzer import PaperAnalyzer
from planner import VideoPlanner
from generator import ManimGenerator
import settings as config

def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from PDF"""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py paper.pdf")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found")
        sys.exit(1)
    
    output_dir = config.OUTPUT_DIR / pdf_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print(f"  PAPER TO VIDEO")
    print("="*60)
    print(f"\n  {pdf_path.name}\n")
    
    # [1/4] Extract
    print("[1/4] Extracting PDF...")
    text = extract_pdf_text(pdf_path)
    print(f"  ✓ {len(text)} chars\n")
    
    # [2/4] Analyze
    print("[2/4] Analyzing...")
    analyzer = PaperAnalyzer()
    analysis = analyzer.analyze(text)
    print(f"  ✓ {len(analysis['concepts'])} concepts\n")
    
    # [3/4] Plan
    print("[3/4] Planning...")
    planner = VideoPlanner()
    videos = planner.plan_videos(analysis)
    print(f"  ✓ {len(videos[0].scenes)} scenes\n")
    
    # [4/4] Generate
    print("[4/4] Generating code...\n")
    generator = ManimGenerator()
    
    for video in videos:
        generator.generate_video_file(video, output_dir)
    
    print("="*60)
    print("  ✅ DONE")
    print("="*60)
    print(f"\n  cd {output_dir}")
    print(f"  python -m manim -pql video1.py Video1\n")

if __name__ == "__main__":
    main()