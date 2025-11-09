# context/extractor.py
"""
Extract rich context from videos for doubt-clearing
"""
import cv2
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from io import BytesIO
from PIL import Image
import sys
sys.path.append(str(Path(__file__).parent.parent))
from models import Video, Scene


class VideoContextExtractor:
    """Extract context from video at specific timestamp"""
    
    def __init__(self, output_dir: Path):
        """
        Args:
            output_dir: Path to output/{job_id}/ directory
        """
        self.output_dir = Path(output_dir)
        self.video_plan = self._load_video_plan()
        self.analysis = self._load_analysis()
    
    def _load_video_plan(self) -> Dict:
        """Load video_plan.json"""
        plan_file = self.output_dir / "video_plan.json"
        if plan_file.exists():
            with open(plan_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_analysis(self) -> Dict:
        """Load analysis.json"""
        analysis_file = self.output_dir / "analysis.json"
        if analysis_file.exists():
            with open(analysis_file, 'r') as f:
                return json.load(f)
        return {}
    
    def extract_context(
        self,
        video_number: int,
        timestamp: float,
        context_window: int = 15
    ) -> Dict:
        """
        Extract comprehensive context at timestamp
        
        Args:
            video_number: Which video (1, 2, 3, etc.)
            timestamp: Time in seconds
            context_window: Seconds before/after to include
            
        Returns:
            Rich context dictionary
        """
        # Find the video file
        video_path = self._find_video_file(video_number)
        
        # Extract frame
        current_frame = self._extract_frame(video_path, timestamp)
        previous_frames = self._extract_frames_range(
            video_path, 
            max(0, timestamp - context_window),
            timestamp,
            num_frames=3
        )
        
        # Map timestamp to scene
        scene_info = self._map_timestamp_to_scene(video_number, timestamp)
        
        # Get surrounding scenes for context
        scene_context = self._get_scene_context(video_number, scene_info['scene_id'])
        
        # Load Manim source code
        manim_code = self._load_manim_code(video_number, scene_info['scene_id'])
        
        # Get subtitles/narration
        narration = scene_info.get('narration', '')
        
        return {
            'video_number': video_number,
            'timestamp': timestamp,
            'current_frame': current_frame,
            'previous_frames': previous_frames,
            'scene_info': scene_info,
            'scene_context': scene_context,
            'manim_code': manim_code,
            'narration': narration,
            'analysis': self.analysis,
            'video_title': self.video_plan.get('videos', [{}])[0].get('title', '')
        }
    
    def _find_video_file(self, video_number: int) -> Optional[Path]:
        """Find the rendered video file"""
        # Try multiple possible paths
        patterns = [
            self.output_dir / 'media' / 'videos' / f'video{video_number}' / '480p15' / f'Video{video_number}.mp4',
            self.output_dir / 'media' / 'videos' / f'video{video_number}' / '1080p60' / f'Video{video_number}.mp4',
        ]
        
        for path in patterns:
            if path.exists():
                return path
        
        return None
    
    def _extract_frame(self, video_path: Path, timestamp: float) -> Optional[str]:
        """Extract single frame as base64 image"""
        if not video_path or not video_path.exists():
            return None
        
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(timestamp * fps)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return None
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')
    
    def _extract_frames_range(
        self,
        video_path: Path,
        start_time: float,
        end_time: float,
        num_frames: int = 3
    ) -> List[str]:
        """Extract multiple frames evenly spaced in time range"""
        if not video_path or not video_path.exists():
            return []
        
        frames = []
        timestamps = [start_time + (end_time - start_time) * i / (num_frames - 1) 
                     for i in range(num_frames)]
        
        for ts in timestamps:
            frame = self._extract_frame(video_path, ts)
            if frame:
                frames.append(frame)
        
        return frames
    
    def _map_timestamp_to_scene(self, video_number: int, timestamp: float) -> Dict:
        """Map timestamp to scene information"""
        videos = self.video_plan.get('videos', [])
        if not videos or video_number > len(videos):
            return {'scene_id': 1, 'scene_title': 'Unknown', 'narration': ''}
        
        video = videos[video_number - 1]
        scenes = video.get('scenes', [])
        
        # Assume each scene is ~60 seconds
        scene_duration = 60.0
        scene_id = int(timestamp / scene_duration) + 1
        scene_id = min(scene_id, len(scenes))
        
        if scene_id <= len(scenes):
            scene = scenes[scene_id - 1]
            return {
                'scene_id': scene_id,
                'scene_title': scene.get('title', ''),
                'narration': scene.get('narration', ''),
                'visual_instructions': scene.get('visual_instructions', '')
            }
        
        return {'scene_id': scene_id, 'scene_title': 'Unknown', 'narration': ''}
    
    def _get_scene_context(self, video_number: int, scene_id: int) -> Dict:
        """Get previous and next scenes for context"""
        videos = self.video_plan.get('videos', [])
        if not videos or video_number > len(videos):
            return {}
        
        video = videos[video_number - 1]
        scenes = video.get('scenes', [])
        
        context = {
            'previous_scene': None,
            'current_scene': None,
            'next_scene': None
        }
        
        if 0 <= scene_id - 1 < len(scenes):
            context['current_scene'] = scenes[scene_id - 1]
        
        if scene_id - 2 >= 0:
            context['previous_scene'] = scenes[scene_id - 2]
        
        if scene_id < len(scenes):
            context['next_scene'] = scenes[scene_id]
        
        return context
    
    def _load_manim_code(self, video_number: int, scene_id: int) -> str:
        """Load relevant Manim source code for the scene"""
        code_file = self.output_dir / f'video{video_number}.py'
        if not code_file.exists():
            return ""
        
        with open(code_file, 'r') as f:
            full_code = f.read()
        
        # Extract the specific scene
        scene_marker = f'# SCENE {scene_id}'
        if scene_marker in full_code:
            start = full_code.index(scene_marker)
            next_scene_marker = f'# SCENE {scene_id + 1}'
            
            if next_scene_marker in full_code:
                end = full_code.index(next_scene_marker)
                return full_code[start:end].strip()
            else:
                # Last scene
                return full_code[start:].strip()
        
        return ""