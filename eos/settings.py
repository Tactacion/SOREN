import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
MODEL = "claude-sonnet-4-5"

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

# Video settings
SCENES_PER_VIDEO = 12
SCENE_DURATION = 30  # seconds
TARGET_VIDEO_COUNT = 1

# Zones (never go outside these)
ZONES = {
    'title': [0, 3.2, 0],
    'left': [-4, 0, 0],
    'center': [0, 0, 0],
    'right': [4, 0, 0],
    'bottom': [0, -2.5, 0]
}

# Colors
COLORS = {
    'blue': '#58C4DD',
    'green': '#8BE17D',
    'orange': '#FFB74D',
    'red': '#FF6188',
    'white': '#FFFFFF'
}