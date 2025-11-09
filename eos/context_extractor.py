"""
Context Extractor - EOS Backend Integration
Extracts rich context from video at any timestamp for doubt handling
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import base64
import PyPDF2


class VideoContextExtractor:
    """
    Extract rich context from video at any timestamp
    Optimized for EOS backend structure
    """

    def __init__(self, project_dir: str, video_path: Optional[str] = None):
        """
        Initialize context extractor

        Args:
            project_dir: Directory containing outputs (e.g., "output/2305.08695v2/")
            video_path: Optional video path for auto-detection
        """
        self.project_dir = Path(project_dir)
        self.video_path = Path(video_path) if video_path else None

        # Load all available data
        self.analysis = self._load_analysis()
        self.scripts = self._load_scripts()
        self.manim_code = self._load_manim_code()
        self.pdf_text = self._load_pdf_text()

        print(f"✅ Context Extractor loaded for {self.project_dir}")

    def extract_context(
        self,
        timestamp: float,
        context_window: float = 30.0
    ) -> Dict:
        """
        Extract comprehensive context at timestamp

        Returns rich context including:
        - Multiple frames (current + 15 before)
        - Voiceover text
        - Manim code
        - Section info
        """
        print(f"\n🔍 Extracting context at {timestamp}s")

        # Get voiceover at this timestamp
        voiceover = self._get_voiceover_at_time(timestamp)

        # Get Manim code section
        manim_code = self._get_manim_code_snippet()

        # Capture multiple frames for context
        frames = self._capture_frames(timestamp, num_frames=16)

        # Get section info
        section_info = self._get_section_info()

        # Get relevant concepts
        key_concepts = self._get_relevant_concepts()

        return {
            'timestamp': timestamp,
            'voiceover_text': voiceover,
            'manim_code': manim_code,
            'frames': frames,  # List of base64 encoded frames
            'section_info': section_info,
            'key_concepts': key_concepts,
            'pdf_text': self.pdf_text,  # Fallback: full PDF text for RAG
        }

    def _load_analysis(self) -> Dict:
        """Load the paper analysis JSON"""
        analysis_files = list(self.project_dir.glob('*_analysis.json'))
        if analysis_files:
            with open(analysis_files[0], 'r') as f:
                return json.load(f)
        return {}

    def _load_scripts(self) -> List[Dict]:
        """Load the generated scripts"""
        script_files = list(self.project_dir.glob('*_scripts.json'))
        if script_files:
            with open(script_files[0], 'r') as f:
                return json.load(f)
        return []

    def _load_manim_code(self) -> str:
        """Load the Manim Python file"""
        py_files = list(self.project_dir.glob('*.py'))
        if py_files:
            with open(py_files[0], 'r') as f:
                return f.read()
        return ""

    def _load_pdf_text(self) -> str:
        """
        Load PDF text as fallback for RAG
        Searches in uploads/ directory and project directory
        """
        try:
            # Check uploads directory
            uploads_dir = self.project_dir.parent.parent / 'uploads'

            # Search for PDFs in both locations
            pdf_paths = []

            if uploads_dir.exists():
                pdf_paths.extend(list(uploads_dir.glob('*.pdf')))

            pdf_paths.extend(list(self.project_dir.glob('*.pdf')))

            if not pdf_paths:
                print("⚠️ No PDF found for fallback RAG")
                return ""

            # Use the first PDF found
            pdf_path = pdf_paths[0]
            print(f"📄 Loading PDF for RAG: {pdf_path.name}")

            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text_chunks = []

                # Extract first 10 pages (or all if less)
                max_pages = min(10, len(pdf_reader.pages))
                for i in range(max_pages):
                    page = pdf_reader.pages[i]
                    text_chunks.append(page.extract_text())

                full_text = '\n'.join(text_chunks)

                # Limit to 8000 chars for context
                if len(full_text) > 8000:
                    full_text = full_text[:8000] + "...\n[PDF text truncated]"

                print(f"✅ Extracted {len(full_text)} chars from PDF")
                return full_text

        except Exception as e:
            print(f"⚠️ Failed to load PDF: {e}")
            return ""

    def _get_voiceover_at_time(self, timestamp: float) -> str:
        """Get the voiceover text at this timestamp"""
        if not self.scripts:
            return "No voiceover available at this time."

        script = self.scripts[0] if self.scripts else {}

        # Get full script text
        if 'script' in script:
            full_script = script['script']
            # Estimate position based on timestamp (assuming ~2 words per second)
            words = full_script.split()
            estimated_position = int(timestamp * 2)

            # Extract window around position
            start_idx = max(0, estimated_position - 30)
            end_idx = min(len(words), estimated_position + 30)

            excerpt = ' '.join(words[start_idx:end_idx])
            return excerpt if excerpt else full_script[:300]

        return "Analyzing visual content at this timestamp."

    def _get_manim_code_snippet(self) -> str:
        """Get relevant Manim code snippet"""
        if not self.manim_code:
            return ""

        # Return first 100 lines as context
        lines = self.manim_code.split('\n')
        return '\n'.join(lines[:100])

    def _capture_frames(
        self,
        timestamp: float,
        num_frames: int = 16
    ) -> List[str]:
        """
        Capture multiple frames (current + previous) for context
        With fallback to single frame if multi-frame capture fails

        Returns list of base64-encoded frame images
        """
        # Find video file
        video_path = self._find_video_file()
        if not video_path:
            print(f"⚠️ No video found - using PDF text fallback only")
            return []

        frames = []

        try:
            # Capture frames: 15 frames before + current frame
            frame_interval = 2.0  # Every 2 seconds
            timestamps = [max(0, timestamp - (i * frame_interval)) for i in range(15, -1, -1)]

            for ts in timestamps:
                frame = self._capture_single_frame(video_path, ts)
                if frame:
                    frames.append(frame)

            if frames:
                print(f"✅ Captured {len(frames)} frames")
            else:
                print(f"⚠️ No frames captured, trying single frame fallback...")
                # Fallback: try to capture just the current frame
                single_frame = self._capture_single_frame(video_path, timestamp)
                if single_frame:
                    frames = [single_frame]
                    print(f"✅ Captured 1 fallback frame at {timestamp}s")

        except Exception as e:
            print(f"⚠️ Frame capture failed: {e}")
            print(f"📄 Falling back to PDF text only")

        return frames

    def _find_video_file(self) -> Optional[Path]:
        """Find the video file"""

        # If video_path was provided, use it
        if self.video_path and self.video_path.exists():
            return self.video_path

        # Search for video in media directory
        media_dir = self.project_dir / "media" / "videos"
        if media_dir.exists():
            for video in media_dir.rglob("*.mp4"):
                if 'partial' not in str(video):
                    return video

        return None

    def _capture_single_frame(self, video_path: Path, timestamp: float) -> Optional[str]:
        """Capture a single frame at timestamp and return as base64"""
        try:
            result = subprocess.run([
                'ffmpeg',
                '-ss', str(timestamp),
                '-i', str(video_path),
                '-vframes', '1',
                '-q:v', '2',
                '-f', 'image2pipe',
                '-vcodec', 'mjpeg',
                '-'
            ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)

            # Encode to base64
            frame_base64 = base64.b64encode(result.stdout).decode('utf-8')
            return frame_base64

        except Exception as e:
            print(f"⚠️ Frame capture failed at {timestamp}s: {e}")
            return None

    def _get_section_info(self) -> Dict:
        """Get section information"""
        if self.scripts:
            script = self.scripts[0]
            return {
                'title': script.get('title', 'Video Section'),
                'description': script.get('description', ''),
            }

        return {'title': 'Video Content', 'description': ''}

    def _get_relevant_concepts(self) -> List[str]:
        """Extract relevant concepts from analysis"""
        if not self.analysis:
            return []

        concepts = []

        if 'key_concepts' in self.analysis:
            concepts.extend(self.analysis['key_concepts'][:5])

        if 'main_contributions' in self.analysis:
            concepts.extend(self.analysis['main_contributions'][:3])

        return concepts
