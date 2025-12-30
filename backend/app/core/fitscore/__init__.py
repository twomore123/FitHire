"""FitScore calculation engine

Deterministic algorithm for matching coaches with jobs based on:
- Certifications
- Experience
- Availability
- Location
- Cultural fit
- Engagement signals
"""

from app.core.fitscore.engine import FitScoreEngine, MatchScore
from app.core.fitscore.presets import WEIGHTING_PRESETS, get_preset, validate_preset

__all__ = [
    "FitScoreEngine",
    "MatchScore",
    "WEIGHTING_PRESETS",
    "get_preset",
    "validate_preset",
]