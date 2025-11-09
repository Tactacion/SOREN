from pathlib import Path
from paper_to_video.processors.pdf_processor import extract_text
from processors.analyzer import PaperAnalyzer
from generators.script import generate_script
from generators.manim import ManimGenerator
from paper_to_video.generators.models import Video
import json
import config
import traceback

class Director:
    def __init__(self):
        self.analyzer = PaperAnalyzer()
        self.manim_gen = ManimGenerator()
    
    def create_video(self, pdf_path: Path):
        print(f"\n{'='*60}")
        print(f"PROCESSING: {pdf_path.name}")
        print(f"{'='*60}\n")
        
        try:
            # Extract text
            print("Step 1: Extracting text...")
            text = extract_text(pdf_path)
            print(f"  Extracted {len(text)} characters")
            
            if len(text) < 100:
                raise ValueError("PDF text too short - might be an image PDF")
            
            # Analyze and plan
            print("\nStep 2: Analyzing paper structure...")
            video = self.analyzer.analyze(text)
            print(f"  Found {len(video.concepts)} concepts")
            print(f"  Planned {len(video.scenes)} scenes")
            
            # Create output directory
            output_dir = config.OUTPUT_DIR / pdf_path.stem
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save plan
            print("\nStep 3: Saving analysis...")
            plan_file = output_dir / "video_plan.json"
            
            plan_data = {
                "title": video.title,
                "total_duration": video.total_duration,
                "concepts": {k: {
                    "name": v.name,
                    "description": v.description,
                    "visual_metaphor": v.visual_metaphor
                } for k, v in video.concepts.items()},
                "scenes": [{
                    "id": s.id,
                    "concepts": s.concepts,
                    "narration": s.narration,
                    "duration": s.duration,
                    "visuals": s.visuals
                } for s in video.scenes]
            }
            
            with open(plan_file, "w") as f:
                json.dump(plan_data, f, indent=2)
            print(f"  Saved to {plan_file}")
            
            # Generate scripts
            scripts = generate_script(video)
            script_file = output_dir / "narration_scripts.json"
            with open(script_file, "w") as f:
                json.dump(scripts, f, indent=2)
            print(f"  Saved scripts to {script_file}")
            
            # Generate Manim code
            print("\nStep 4: Generating Manim animations...")
            successful = 0
            failed = []
            
            for scene in video.scenes:
                try:
                    print(f"  Generating Scene {scene.id}...")
                    code = self.manim_gen.generate_scene(scene, video)
                    
                    scene_file = output_dir / f"scene_{scene.id}.py"
                    scene_file.write_text(code)
                    print(f"    Success: {scene_file}")
                    successful += 1
                    
                except Exception as e:
                    print(f"    Failed: {e}")
                    failed.append(scene.id)
                    traceback.print_exc()
            
            # Summary
            print(f"\n{'='*60}")
            print("GENERATION COMPLETE")
            print(f"{'='*60}")
            print(f"Output directory: {output_dir}")
            print(f"Scenes generated: {successful}/{len(video.scenes)}")
            
            if failed:
                print(f"Failed scenes: {failed}")
            
            print(f"\nTo render the video:")
            print(f"  cd {output_dir}")
            for i in range(1, successful + 1):
                print(f"  manim -pql scene_{i}.py Scene{i}")
            
            print(f"\nTo render all at once:")
            print(f"  cd {output_dir} && for f in scene_*.py; do manim -pql $f; done")
            
        except Exception as e:
            print(f"\nERROR: {e}")
            traceback.print_exc()
            return False
        
        return True