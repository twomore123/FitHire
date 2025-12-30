"""FitScore weighting presets

Defines different scoring emphasis strategies for different job types.
"""

from typing import Dict

# Weighting presets for FitScore calculation
WEIGHTING_PRESETS: Dict[str, Dict[str, float]] = {
    "balanced": {
        "certifications": 0.25,
        "experience": 0.20,
        "availability": 0.15,
        "location": 0.15,
        "cultural_fit": 0.15,
        "engagement": 0.10,
    },
    "experience_heavy": {
        "certifications": 0.20,
        "experience": 0.35,  # Emphasized
        "availability": 0.10,
        "location": 0.10,
        "cultural_fit": 0.15,
        "engagement": 0.10,
    },
    "culture_heavy": {
        "certifications": 0.15,
        "experience": 0.15,
        "availability": 0.10,
        "location": 0.10,
        "cultural_fit": 0.40,  # Emphasized
        "engagement": 0.10,
    },
    "availability_focused": {
        "certifications": 0.20,
        "experience": 0.15,
        "availability": 0.35,  # Emphasized
        "location": 0.10,
        "cultural_fit": 0.10,
        "engagement": 0.10,
    },
}


def validate_preset(preset_name: str) -> bool:
    """
    Validate that a preset name exists and weights sum to 1.0

    Args:
        preset_name: Name of the preset to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if preset_name not in WEIGHTING_PRESETS:
        return False

    weights = WEIGHTING_PRESETS[preset_name]
    total = sum(weights.values())

    # Allow small floating point error
    return abs(total - 1.0) < 0.001


def get_preset(preset_name: str) -> Dict[str, float]:
    """
    Get weighting values for a preset

    Args:
        preset_name: Name of the preset

    Returns:
        Dict[str, float]: Mapping of score component to weight

    Raises:
        ValueError: If preset name doesn't exist
    """
    if preset_name not in WEIGHTING_PRESETS:
        raise ValueError(
            f"Unknown preset '{preset_name}'. "
            f"Available: {', '.join(WEIGHTING_PRESETS.keys())}"
        )

    return WEIGHTING_PRESETS[preset_name]
