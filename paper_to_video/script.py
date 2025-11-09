from paper_to_video.generators.models import Scene, Video
from typing import List

def generate_script(video: Video) -> List[dict]:
    scripts = []
    for scene in video.scenes:
        scripts.append({
            "scene_id": scene.id,
            "text": scene.narration,
            "duration": scene.duration
        })
    return scripts