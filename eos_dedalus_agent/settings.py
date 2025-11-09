# settings.py
# ============================================================================
# CONFIGURATION MANAGEMENT FOR DEDALUS VIDEO PIPELINE
# ============================================================================
# Centralized configuration with validation and sensible defaults

import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# ============================================================================
# API KEYS
# ============================================================================

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY")
DEDALUS_API_KEY = os.getenv("DEDALUS_API_KEY")

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Primary model for all LLM tasks (analysis, planning, generation)
# Using OpenAI GPT-4 as workaround for Dedalus Anthropic bug
MODEL = "openai/gpt-4"  # GPT-4 (workaround for Dedalus bug)
# MODEL = "anthropic/claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5 (has Dedalus bug)

# Model for fixing Manim errors (can be same or different)
# Using same model for consistency, but could use a cheaper model for simple fixes
FIXER_MODEL = "openai/gpt-4"  # GPT-4 (workaround for Dedalus bug)
# FIXER_MODEL = "anthropic/claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5 (has Dedalus bug)

# Alternative models (uncomment to switch):
# MODEL = "anthropic/claude-3-opus-20240229"  # More powerful but slower/expensive
# MODEL = "anthropic/claude-3-haiku-20240307"  # Faster and cheaper but less capable
# FIXER_MODEL = "anthropic/claude-3-haiku-20240307"  # Cheaper for simple fixes

# ============================================================================
# DIRECTORY STRUCTURE
# ============================================================================

# Base directory (where this settings.py file lives)
BASE_DIR = Path(__file__).parent.resolve()

# Output directory for all generated content
OUTPUT_DIR = BASE_DIR / "output"

# Upload directory for incoming PDFs
UPLOAD_DIR = BASE_DIR / "uploads"

# Media directory for Manim output (automatically created by Manim)
MEDIA_DIR = BASE_DIR / "media"

# ============================================================================
# PIPELINE CONFIGURATION
# ============================================================================

# Maximum number of render retry attempts after fixing errors
MAX_RENDER_RETRIES = 3

# Manim render quality (-ql = low, -qm = medium, -qh = high, -qk = 4k)
# Low quality is faster for development, use high for production
MANIM_QUALITY = "-ql"  # Change to -qh for final renders

# Timeout for Manim rendering (in seconds)
RENDER_TIMEOUT = 600  # 10 minutes

# ============================================================================
# ELEVENLABS VOICE CONFIGURATION
# ============================================================================

# Voice to use for narration (options: Adam, Antoni, Arnold, Bella, Domi, Elli, Josh, Rachel, Sam)
ELEVENLABS_VOICE = "Adam"  # Deep, professional male voice

# Alternative voices:
# "Bella" - Warm, friendly female voice
# "Rachel" - Calm, informative female voice
# "Sam" - Energetic, young male voice

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log level for the application
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Enable debug mode for more verbose logging
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

# ============================================================================
# DIRECTORY INITIALIZATION
# ============================================================================

def init_directories():
    """Create all necessary directories if they don't exist."""
    directories = [OUTPUT_DIR, UPLOAD_DIR]

    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

# Initialize on import
init_directories()

# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================

def validate_config() -> tuple[bool, list[str]]:
    """
    Validates that all required configuration is present.

    Returns:
        tuple: (is_valid, list of error messages)
    """
    errors = []

    # Check required API keys
    if not ANTHROPIC_KEY:
        errors.append("ANTHROPIC_API_KEY is not set in .env file")

    if not ELEVENLABS_API_KEY:
        errors.append("ELEVENLABS_API_KEY (or ELEVEN_API_KEY) is not set in .env file")

    if not DEDALUS_API_KEY:
        errors.append("DEDALUS_API_KEY is not set in .env file")

    # Check model configuration
    if not MODEL:
        errors.append("MODEL is not configured")

    # Check directories are writable
    try:
        test_file = OUTPUT_DIR / ".write_test"
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        errors.append(f"OUTPUT_DIR is not writable: {e}")

    is_valid = len(errors) == 0
    return is_valid, errors


def print_config():
    """Prints current configuration (for debugging)."""
    print("\n" + "="*80)
    print("CONFIGURATION")
    print("="*80)
    print(f"Base Directory: {BASE_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Upload Directory: {UPLOAD_DIR}")
    print(f"Primary Model: {MODEL}")
    print(f"Fixer Model: {FIXER_MODEL}")
    print(f"Manim Quality: {MANIM_QUALITY}")
    print(f"Render Timeout: {RENDER_TIMEOUT}s")
    print(f"Max Render Retries: {MAX_RENDER_RETRIES}")
    print(f"ElevenLabs Voice: {ELEVENLABS_VOICE}")
    print(f"Debug Mode: {DEBUG_MODE}")
    print(f"API Keys Configured: ", end="")
    keys_status = []
    if ANTHROPIC_KEY:
        keys_status.append("Anthropic ✅")
    else:
        keys_status.append("Anthropic ❌")
    if ELEVENLABS_API_KEY:
        keys_status.append("ElevenLabs ✅")
    else:
        keys_status.append("ElevenLabs ❌")
    if DEDALUS_API_KEY:
        keys_status.append("Dedalus ✅")
    else:
        keys_status.append("Dedalus ❌")
    print(", ".join(keys_status))
    print("="*80 + "\n")


# ============================================================================
# EXPORT CONFIGURATION SUMMARY
# ============================================================================

__all__ = [
    'ANTHROPIC_KEY',
    'ELEVENLABS_API_KEY',
    'DEDALUS_API_KEY',
    'MODEL',
    'FIXER_MODEL',
    'BASE_DIR',
    'OUTPUT_DIR',
    'UPLOAD_DIR',
    'MEDIA_DIR',
    'MAX_RENDER_RETRIES',
    'MANIM_QUALITY',
    'RENDER_TIMEOUT',
    'ELEVENLABS_VOICE',
    'LOG_LEVEL',
    'DEBUG_MODE',
    'validate_config',
    'print_config'
]
